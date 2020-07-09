# An illustration of ZMQ's support for the Pipeline a.k.a. Push/Pull topology.
# Reference:
# https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pushpull.html

import zmq
import sys
from random import randrange


def main():
    upstream_port = "5810"
    downstream_port = "5811"
    if len(sys.argv) >= 3:
        upstream_port = sys.argv[1]
        print("Overriding default upstream port to:", upstream_port)
        _ = int(upstream_port)
        downstream_port = sys.argv[2]
        print("Overriding default downstream port to:", downstream_port)
        _ = int(downstream_port)

    # We tag each of these stage nodes with an ID, in order to determine
    # how well ZMQ interleaves messages from the source node to stage nodes.
    my_id = randrange(1, 10000)

    # We create this stage with ZMQ socket types "zmq.PULL" and "zmq.PUSH"
    # for the upstream and downstream connection respectively.
    context = zmq.Context()
    upstream_socket = context.socket(zmq.PULL)
    upstream_socket.connect("tcp://localhost:" + upstream_port)
    downstream_socket = context.socket(zmq.PUSH)
    downstream_socket.connect("tcp://localhost:" + downstream_port)
    print("I am a pipeline stage, pulling from port {} and pushing to port {}"
          .format(upstream_port, downstream_port))

    while True:
        upstream_msg = upstream_socket.recv_json()
        # We assume the processing we do in this stage generates
        # 1 downstream message for every 5 upstream messages.
        upstream_msg_id = upstream_msg['msg_id']
        if upstream_msg_id % 5 == 0:
            downstream_msg = {'stage_id': my_id, 'msg_id': upstream_msg_id}
            downstream_socket.send_json(downstream_msg)


main()
