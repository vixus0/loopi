#!/usr/bin/env python

import glob
import wave
import tempfile
import os
import sys
import math
from subprocess import call
from functools import reduce


def lcm(a, b):
    return a * b // math.gcd(a, b)


wavs = sorted(glob.glob(os.path.join(sys.argv[1], '*.wav')))
tmpd = tempfile.mkdtemp()

for wav in wavs:
    print(f'Converting {wav} to 48kHz')
    out = os.path.join(tmpd, os.path.basename(wav))
    call(['ffmpeg', '-loglevel', 'fatal', '-i', wav, '-ar', '48000', out])

new_wavs = [os.path.join(tmpd, os.path.basename(w)) for w in wavs]
lengths = []

for w in new_wavs:
    with wave.open(w, 'r') as wfile:
        lengths.append(wfile.getnframes())

ratios = [int(math.ceil(v/lengths[0])) if v > 0 else 1 for v in lengths]
print(f'Lengths: {lengths}')
print(f'Ratios: {ratios}')
lcm_all = reduce(lcm, ratios)
mult = [lcm_all // r for r in ratios]
print(f'Multiply factors: {mult}')

loop_wavs = [w.replace('.wav', '') + '_loop.wav' for w in new_wavs]

for i, w in enumerate(new_wavs):
    looped_w = loop_wavs[i]
    print(f'Looping {w} x {mult[i]}')

    with wave.open(w, 'r') as wfile_orig:
        frames = wfile_orig.readframes(lengths[i])

        with wave.open(looped_w, 'w') as wfile_loop:
            wfile_loop.setnchannels(wfile_orig.getnchannels())
            wfile_loop.setframerate(wfile_orig.getframerate())
            wfile_loop.setsampwidth(wfile_orig.getsampwidth())
            wfile_loop.writeframes(frames * mult[i])

    os.remove(w)

merge_wav = os.path.join('merged', os.path.split(sys.argv[1])[-1].replace('/', '') + '.wav')
input_wavs = []

for i, w in enumerate(loop_wavs):
    if lengths[i] > 0:
        input_wavs.append('-i')
        input_wavs.append(w)

merge_cmd = ['ffmpeg', '-loglevel', 'fatal']

if len(input_wavs)//2 > 1:
    merge_cmd.extend(['-filter_complex', 'amerge'])

merge_cmd.extend(input_wavs)
merge_cmd.append(merge_wav)
print(f'Merging: {merge_cmd}')
call(merge_cmd)
call(['mpv', merge_wav])

for w in loop_wavs:
    os.remove(w)
os.removedirs(tmpd)
