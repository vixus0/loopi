#!/usr/bin/env python2

from mididings import *
from mididings.extra.osc import *
from liblo import Address
from datetime import datetime

def jack_capture_cmd():
    return 'jack_capture --format ogg --osc 9898 -fp /mnt/mrbox/loops/capture/track_'

print('Loopidings')

config(
    client_name = 'loopidings'
    )

run(
Filter(NOTEON) >> [
    KeyFilter(notes=[3]) % System('bash /home/vixus/git/loopi/sl-dump-tracks'),
    KeyFilter(notes=[4]) % System(jack_capture_cmd()),
    KeyFilter(notes=[5]) %  SendOSC(Address(9898), '/jack_capture/stop')
    ]
)
