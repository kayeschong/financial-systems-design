# An illustration of ZMQ's support for the Publish/Subscribe topology.
# Reference:
# https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pubsub.html

import zmq
import sys


def main():
    # SUBJECT TO CHANGE:
    num_requested_stories = 10
    preferred_topic = 'Sports'

    ports = ["5800"]  # Our default publisher port.
    # Here we are illustrating the less common, more interesting use case where
    # one subscriber connects to multiple publishers.  In this scenario ZMQ
    # interleaves the receipt of the publications, to ensure no one publisher
    # overwhelms the subscriber.
    if len(sys.argv) > 1:
        ports = sys.argv[1:]
        print("Overriding default port to:", ', '.join([p for p in ports]))
        assert len(ports) == len(set(ports)), "All port numbers must be unique"
        _ = [int(p) for p in ports]

    # We create this subscriber with ZMQ socket type "zmq.SUB".
    context = zmq.Context()
    print("Connecting to publisher(s)...")
    socket = context.socket(zmq.SUB)
    # Here we are using one socket object containing multiple connections.
    # Compare this to our example request/reply client, which demonstrates
    # multiple sockets each containing one connection.
    for port in ports:
        socket.connect("tcp://localhost:" + port)

    # The ability to filter subscribed messages is built in.
    socket.setsockopt_string(zmq.SUBSCRIBE, preferred_topic)

    for i in range(num_requested_stories):
        message = socket.recv().decode("utf-8")
        print('Received story {}: {}'.format(i+1, message))


main()
