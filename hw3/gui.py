import zmq
import sys
import PySimpleGUI as sg

sg.theme('Light Grey1')

balance_size = (20, 1)
balance_frame = [
    [
        sg.Text('Shares', size=balance_size), 
        sg.Text('Cash', size=balance_size)
    ],
    [
        sg.Text(0, key='shares', size=balance_size, background_color='white',),
        sg.Text(0, key='cash', size=balance_size, background_color='white',)
    ],
]

deposit_size = (20, 1)
deposit_frame = [
    [
        sg.Input(key="deposit_amount", size=deposit_size),
        sg.Button("Deposit", key='deposit_cash')
    ],
]

buy_size = (20, 1)
buy_frame = [
    [
        sg.Text("Quantity", size=buy_size), 
        sg.Text("Price per Share", size=buy_size)
    ],
    [
        sg.Input(key="buy_qty", size=buy_size),
        sg.Input(key="buy_price", size=buy_size),
        sg.Button("Buy", key='buy')
    ],
]

sell_size = (20, 1)
sell_frame = [
    [
        sg.Text("Quantity", size=sell_size),
        sg.Text("Price per Share", size=sell_size)
    ],
    [
        sg.Input(key="sell_qty", size=sell_size),
        sg.Input(key="sell_price", size=sell_size),
        sg.Button("Sell", key='sell')
    ],
]

layout = [[
        sg.Column(
            [
                [sg.Frame('Balances', balance_frame)],
                [sg.Frame('Deposit Cash', deposit_frame)],
                [sg.Frame('Buy Shares', buy_frame)],
                [sg.Frame('Sell Shares', sell_frame)],
                [sg.Button('Exit', button_color=("white", "red"))],
                [sg.Text("VWAP placeholder",
                         key='get_latest_vwaps',
                         size=(80, 1),
                         justification='center',),]
            ],
            element_justification='center'
        )]
]

window = sg.Window('Window Title', layout) #, font="Gotham 20")


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


while True:

    event, values = window.read(timeout=10)
    # print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        # socket.send_string('shutdown_server')
        # message = socket.recv().decode("utf-8")
        break

    elif event == '__TIMEOUT__':
        pass

    elif event in ("deposit_cash", "buy", "sell"):
        if event == "deposit_cash":
            cmd = event + " " + values['deposit_amount']

        elif event == "buy":
            cmd = event + " " + values['buy_qty'] + " " + values['buy_price']

        elif event == "sell":
            cmd = event + " " + values['sell_qty'] + " " + values['sell_price']

        socket.send_string(cmd)
        message = socket.recv().decode("utf-8")
        print(message)

    socket.send_string('get_latest_vwaps')
    latest_vwap = socket.recv().decode("utf-8")
    window['get_latest_vwaps'].update(latest_vwap) # TODO: Formatting

    socket.send_string('get_share_balance')
    message = socket.recv().decode("utf-8")
    latest_share_balance = message.split(" ")[1]
    window['shares'].update(latest_share_balance)

    socket.send_string('get_cash_balance')
    message = socket.recv().decode("utf-8")
    latest_cash_balance = message.split(" ")[1]
    window['cash'].update(latest_cash_balance)


window.close()
