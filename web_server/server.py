#!/usr/bin/env python

from gevent import monkey
monkey.patch_all()
monkey.patch_sys(stdin=True, stdout=False, stderr=False)
import gevent
from gevent.queue import Queue
import signal
import sys
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

from formatter import process_log
from web_server import make_server
import random
import datetime


q = Queue()

from anypubsub import create_pubsub

pubsub = create_pubsub('memory')

EQUIPS = ['RE002', 'RE003', 'RE004']

def gettimestr():
    t = datetime.datetime.now()
    return t.strftime('%Y-%m-%d %H:%M:%S')

def producer():
    while True:
        line = sys.stdin.readline()
        process_log(line, q.put)

def dummy_producer():
    i = 0

    while True:
        #process_log("Msg %d..." % i, q.put)
        rad_val = random.uniform(0, 100)
        equip = random.choice(EQUIPS)
        msg = {
            'id' : equip,
            'time' : gettimestr(),
            'readvalue' : rad_val
        }
        pubsub.publish('rms_read', msg)
        #print msg

        i += 1
        gevent.sleep(1)
        if i > 10:
            i = 0




class LogNamespace(BaseNamespace, BroadcastMixin):
    def recv_connect(self):
        def sendlogs():
            while True:
                #val = q.get(True)
                #self.broadcast_event('log', {'line': val})
                val = self.subscriber.next()
                self.emit('log', val)

        self.subscriber = pubsub.subscribe('rms_read')

        print 'Client connected...'
        self.spawn(sendlogs)


class RMSNamespace(BaseNamespace, BroadcastMixin):
    def recv_connect(self):
        def sendRMSdata():
            while True:
                #val = q.get(True)
                #self.broadcast_event('log', {'line': val})
                val = self.subscriber.next()
                self.emit('RMSdata', val)

        self.subscriber = pubsub.subscribe('rms_read')

        print 'Client connected...'
        self.spawn(sendRMSdata)




def main():
    gevent.signal(signal.SIGQUIT, gevent.kill)


    server = make_server({
        '/logs': LogNamespace,
        '/rms' : RMSNamespace
    })


    greenlets = [
        gevent.spawn(producer),
	    gevent.spawn(dummy_producer)
    ]

    try:
        server.start()
        print 'Log webserver running on http://0.0.0.0:51324'
        gevent.joinall(greenlets)
    except KeyboardInterrupt:
        print "Exiting..."


if __name__ == '__main__':
    main()
