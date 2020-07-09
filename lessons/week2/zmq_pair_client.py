# An illustration of ZMQ's support for the Pair topology.
# Reference:
# https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pair.html .

import zmq
import sys


# To make our cleanup easier, this client can ask the server to quit.
# (Not a good idea in general.)
def send_quit_request(socket):
    socket.send_string("quit")
    msg = socket.recv()  # The server will acknowledge, then quit.
    print("Received final reply [", msg.decode("utf-8"), "]")


def main():
    # SUBJECT TO CHANGE:
    num_requests = 10

    port = "5780"  # Our default server port.
    if len(sys.argv) > 1:
        port = sys.argv[1]
        print("Overriding default port to", port)
        _ = int(port)

    # We create this client with ZMQ socket type "zmq.PAIR".
    context = zmq.Context()
    print("Connecting to server...")
    socket = context.socket(zmq.PAIR)
    socket.connect("tcp://localhost:" + port)

    for i in range(num_requests):
        print("Sending request", i+1, "...")
        # socket.send("Hello")  Won't work because "Hello" will be sent in
        # Unicode, whereas send_string() defaults to utf-8.
        socket.send_string("Hello from Pair client (" + str(i+1) + ")")
        message = socket.recv()  # Block until the server has replied.
        print("Received reply", i+1, "[", message.decode("utf-8"), "]")

    send_quit_request(socket)


main()
