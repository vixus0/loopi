#!/usr/bin/env python2

from mididings import *
from mididings.extra.osc import *
from liblo import Address
from datetime import datetime
from os import environ

rec = False

jack_capture_stop = SendOSC(Address(9898), '/jack_capture/stop')

def jack_capture_cmd():
    return 'jack_capture --format ogg --osc 9898 -fp '+environ['RECORDINGS']

def rec_toggle(event):
    if rec:
      rec = False
      return jack_capture_stop
    else:
      rec = True
      return System(jack_capture_cmd())

print('Loopidings')

config(
    client_name = 'loopidings'
    )

run(
Filter(NOTEON) >> [
    KeyFilter(notes=[5]) % Process(rec_toggle)
    ]
)
