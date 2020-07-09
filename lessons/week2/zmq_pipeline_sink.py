# An illustration of ZMQ's support for the Pipeline a.k.a. Push/Pull topology.
# Reference:
# https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pushpull.html

import zmq
import sys
from collections import Counter

# To run the server at a non-default port, the user provides the alternate port
# number on the command line.
port = "5811"  # Our default port.
if len(sys.argv) > 1:
    port = sys.argv[1]
    print("Overriding default port to", port)
    _ = int(port)

# We create the pipeline sink with ZMQ socket type "zmq.PULL".
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:" + port)
print("I am a pipeline sink, now alive on port", port)

counts_by_stage_id = Counter()
num_sink_messages = 20000
for i in range(num_sink_messages):
    sink_message = socket.recv_json()
    stage_id = sink_message['stage_id']
    counts_by_stage_id[stage_id] += 1

# Similar counts for each stage ID demonstrate that ZMQ does a good job
# interleaving messages from the source to the stage nodes.
print('Message counts for each stage node:', str(counts_by_stage_id.values()))
