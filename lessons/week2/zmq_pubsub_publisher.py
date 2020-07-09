# An illustration of ZMQ's support for the Publish/Subscribe topology.
# Reference:
# https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pubsub.html

import zmq
import time
import sys
from random import choice, randrange

# To run the server at a non-default port, the user provides the alternate port
# number on the command line.
port = "5800"  # Our default port.
if len(sys.argv) > 1:
    port = sys.argv[1]
    print("Overriding default port to", port)
    _ = int(port)

# We create the publisher with ZMQ socket type "zmq.PUB".
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:" + port)
print("I am a Pub/Sub publisher, now alive and publishing to port", port)

# SUBJECT TO CHANGE:
available_topics = ['Headlines', 'Business', 'Sports', 'Weather', 'People']

while True:
    topic = choice(available_topics)
    story_id = randrange(10000, 99999)
    message = '{} {}'.format(topic, story_id)
    print('Publishing:', message)
    socket.send_string(message)
    time.sleep(1)
