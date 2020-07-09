# An illustration of ZMQ's support for the Request/Reply topology.
# Reference:
# http://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/client_server.html .

import zmq
import sys


# To make our cleanup easier, this client can ask each server to quit.
# (Not a good idea in general!)
def send_quit_request(socket):
    socket.send_string("quit")
    msg = socket.recv()  # The server will acknowledge, then quit.
    print("Received final reply [", msg.decode("utf-8"), "]")


def main():
    # SUBJECT TO CHANGE:
    num_requests = 5

    ports = ["5790"]  # Our default server port.
    # We allow this client to send its requests to multiple servers.
    # ZMQ will automatically interleave the requests among them.
    if len(sys.argv) > 1:
        ports = sys.argv[1:]
        print("Overriding default port to:", ', '.join([p for p in ports]))
        assert len(ports) == len(set(ports)), "All port numbers must be unique"
        _ = [int(p) for p in ports]

    # We create this client with ZMQ socket type "zmq.REQ".
    context = zmq.Context()
    print("Connecting to server(s)...")
    # We have an important choice to make:  either *multiple* socket objects
    # each containing *one* server connection, or *one* socket object
    # containing *multiple* server connections.
    # Here we are demonstrating multiple socket objects.  Compare this to our
    # example publish/subscribe client, which demonstrates one socket object
    # containing multiple connections.
    sockets = []
    for port in ports:
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:" + port)
        sockets.append(socket)

    # After sending a request, we must wait for a reply.
    for i in range(num_requests):
        print("Sending request", i+1, "...")
        # Since we have chosen to have multiple socket objects, we are
        # responsible for routing our requests to particular servers.
        # If instead we had one socket containing multiple connections, then
        # ZMQ would decide how to route our requests to particular servers.
        for socket in sockets:
            # socket.send("Hello")  Won't work because "Hello" will be sent in
            # Unicode, whereas send_string() defaults to utf-8.
            socket.send_string("Hello from Req/Rep client (" + str(i+1) + ")")
            message = socket.recv()  # Block until the server has replied.
            print("Received reply", i+1, "[", message.decode("utf-8"), "]")

    for socket in sockets:
        send_quit_request(socket)


main()
