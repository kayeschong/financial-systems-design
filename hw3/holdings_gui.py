import zmq
import sys
import PySimpleGUI as sg
import time

sg.theme('LightBlue')
balance_size = (20, 1)
balance_frame = [
    [
        sg.Text('Shares', size=balance_size), 
        sg.Text('Cash', size=balance_size)
    ],
    [
        sg.Text("Please start server", key='shares', size=balance_size, background_color='white',),
        sg.Text("Pleaser start server", key='cash', size=balance_size, background_color='white',)
    ],
]

deposit_size = (20, 1)
deposit_frame = [
    [
        sg.Input(key="deposit_amount", size=deposit_size, background_color='white'),
        sg.Button("Deposit", key='deposit_cash', button_color=("white", "blue"))
    ],
]

buy_size = (20, 1)
buy_frame = [
    [
        sg.Text("Quantity", size=buy_size), 
        sg.Text("Price per Share", size=buy_size)
    ],
    [
        sg.Input(key="buy_qty", size=buy_size, background_color='white'),
        sg.Input(key="buy_price", size=buy_size, background_color='white'),
        sg.Button("Buy", key='buy', button_color=("white", "blue"))
    ],
]

sell_size = (20, 1)
sell_frame = [
    [
        sg.Text("Quantity", size=sell_size),
        sg.Text("Price per Share", size=sell_size)
    ],
    [
        sg.Input(key="sell_qty", size=sell_size, background_color='white'),
        sg.Input(key="sell_price", size=sell_size, background_color='white'),
        sg.Button("Sell", key='sell', button_color=("white", "blue"))
    ],
]

layout = [[
        sg.Column(
            [
                [sg.Frame('Balances', balance_frame)],
                [sg.Frame('Deposit Cash', deposit_frame)],
                [sg.Frame('Buy Shares', buy_frame)],
                [sg.Frame('Sell Shares', sell_frame)],
                [sg.Button('Close Server & Quit', button_color=("white", "darkred"))],
                [sg.Text("VWAP placeholder", key='get_latest_vwaps', size=(80, 1), justification='center',)]
            ],
            element_justification='center'
        )]
]

window = sg.Window('Holdings Manager', layout, font="Helvetica 12", icon='sutd.ico')


port = "5890"  # Our default server port.
if len(sys.argv) > 1:
    port = sys.argv[1]
    print("Overriding default port to", port)
    ignored = int(port)

context = zmq.Context()
# Using "zmq.PAIR" means there is exactly one server for each client
# and vice-versa.  For this application, zmq.PAIR is more appropriate
# than zmq.REQ + zmq.REP (make sure you understand why!).
socket = context.socket(zmq.PAIR)
print("Connecting to server...")
socket.connect("tcp://localhost:" + port)


# Update with initial values in server
event, values = window.read(timeout=100)

socket.send_string('get_share_balance')
message = socket.recv().decode("utf-8")
latest_share_balance = message.split(" ")[1]
window['shares'].update(latest_share_balance)

socket.send_string('get_cash_balance')
message = socket.recv().decode("utf-8")
latest_cash_balance = message.split(" ")[1]
window['cash'].update(latest_cash_balance)

socket.send_string('get_latest_vwaps')
latest_vwap = socket.recv().decode("utf-8").split()
_, buy_vwap, sell_vwap = latest_vwap

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

vwap_text = f"{current_time}: Buy VWAP={buy_vwap}, Sell VWAP={sell_vwap}"
window['get_latest_vwaps'].update(vwap_text)


while True:

    # Timeout to update VWAPS 10 times per sec
    event, values = window.read(timeout=100)
    # print(event, values)

    if event in (sg.WIN_CLOSED, 'Close Server & Quit'):
        # # Shutdown server when gui closes
        socket.send_string('shutdown_server')
        # message = socket.recv().decode("utf-8")
        break

    elif event in ("deposit_cash", "buy", "sell"):
        if event == "deposit_cash":
            cmd = event + " " + values['deposit_amount']

        elif event == "buy":
            cmd = event + " " + values['buy_qty'] + " " + values['buy_price']

        elif event == "sell":
            cmd = event + " " + values['sell_qty'] + " " + values['sell_price']

        socket.send_string(cmd)
        message = socket.recv().decode("utf-8")
        is_error = message.split()[0] == '[ERROR]'
        if is_error:
            sg.Popup(message, title='error', button_color=('white', 'red'), font="Helvetica 12")
            # Change button color to yellow when invalid input
            window[event].update(button_color=("black", "yellow"))
        else:
            # Change button color to original when valid input given
            window[event].update(button_color=("white", "blue"))

            # Update balance if valid input
            socket.send_string('get_share_balance')
            message = socket.recv().decode("utf-8")
            latest_share_balance = message.split(" ")[1]
            window['shares'].update(latest_share_balance)

            socket.send_string('get_cash_balance')
            message = socket.recv().decode("utf-8")
            latest_cash_balance = message.split(" ")[1]
            window['cash'].update(latest_cash_balance)

    # "Async" update of vwap 10 times per sec, but server only updates once per 10 sec...
    socket.send_string('get_latest_vwaps')
    latest_vwap = socket.recv().decode("utf-8").split()
    _, buy_vwap, sell_vwap = latest_vwap

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    vwap_text = f"{current_time}: Buy VWAP={buy_vwap}, Sell VWAP={sell_vwap}"
    window['get_latest_vwaps'].update(vwap_text)


window.close()
