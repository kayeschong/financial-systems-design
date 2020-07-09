# An illustration of ZMQ's support for the Pipeline a.k.a. Push/Pull topology.
# Reference:
# https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pushpull.html

import zmq
import sys

# To run the server at a non-default port, the user provides the alternate port
# number on the command line.
port = "5810"  # Our default port.
if len(sys.argv) > 1:
    port = sys.argv[1]
    print("Overriding default port to", port)
    _ = int(port)

# We create the pipeline source with ZMQ socket type "zmq.PUSH".
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind("tcp://*:" + port)
print("I am a pipeline source, now alive on port", port)

# N.B. The following code will hang unless the other "downstream" stages of the
# pipeline have already been started.
num_source_messages = 100000
for i in range(num_source_messages):
    source_message = {'msg_id': i}
    socket.send_json(source_message)
