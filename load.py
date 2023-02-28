#!/usr/bin/env python3

import sys
import threading
import time

import redis


def wait_for_message(pubsub, count):
    while True:
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message is not None:
            print("recvd")
            count -= 1
            if count == 0:
                return message
        time.sleep(0.01)


N = 200
PUBCOUNT = 100
MESSAGESIZE = 10000
r = redis.Redis()

ps = [r.pubsub() for _ in range(N)]
for p in ps:
    p.subscribe("c")

ts = [
    threading.Thread(group=None, target=wait_for_message, args=(p, PUBCOUNT))
    for p in ps
]
print("start reader threads", file=sys.stderr)
for t in ts:
    t.start()

print("start pub", file=sys.stderr)
for _ in range(PUBCOUNT):
    r.publish("c", "some message:" + "a" * MESSAGESIZE)

# this doesn't seem to be needed, but it is intended to wait
# for the threads to finish
for t in ts:
    t.join()
