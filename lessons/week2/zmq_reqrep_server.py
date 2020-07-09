# An illustration of ZMQ's support for the Request/Reply topology.
# Reference:
# http://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/client_server.html .

import zmq
import time
import sys

# To run the server at a non-default port, the user provides the alternate port
# number on the command line.
port = "5790"  # Our default port.
if len(sys.argv) > 1:
    port = sys.argv[1]
    print("Overriding default port to", port)
    _ = int(port)

# We create the server with ZMQ socket type "zmq.REP".
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:" + port)
print("I am a Request/Reply server, now alive and listening on port", port)

while True:
    message = socket.recv()  # Blocks until the client has sent a message.
    decoded = message.decode("utf-8")
    print("Received: ", decoded)
    # To make our cleanup easier, we support a "quit" request from the client:
    if decoded == "quit":
        socket.send_string("Good-bye from port " + port)  # Defaults to utf-8
        sys.exit(0)
    else:
        time.sleep(1)  # Spend some time processing the request.
        socket.send_string("Hello from port " + port)  # Defaults to utf-8
