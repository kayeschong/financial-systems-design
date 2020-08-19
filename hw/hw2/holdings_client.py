# The client code for 40.317 Homework 1.  This code is complete.
# It assumes the server runs on the same machine.

import zmq
import sys

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
    cmd = input("Holdings Manager> ")
    if cmd == "":
        # Don't contact the server every time the user presses the Enter key.
        continue
    if cmd.lower() in {'quit', 'exit'}:
        sys.exit(0)
    # The server validates the requests, so we need not validate them here.
    socket.send_string(cmd)
    message = socket.recv()
    print(message.decode("utf-8"))
