#! /usr/bin/env python

import sys
from aubio import tempo, source
from play_song import play_song
import time

win_s = 512                 # fft size
hop_s = win_s // 2          # hop size

filename = './classification/neillversion/02Injection.flac.wav'

samplerate = 0
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate
o = tempo("default", win_s, hop_s, samplerate)

# tempo detection delay, in samples
# default to 4 blocks delay to catch up with
delay = 4. * hop_s

# list of beats, in samples
beats = []

beat_times = []

# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    is_beat = o(samples)
    if is_beat:
        this_beat = int(total_frames - delay + is_beat[0] * hop_s)
        print("%f" % (this_beat / float(samplerate)))
        beats.append(this_beat)
        beat_times.append(this_beat / float(samplerate))
    total_frames += read
    if read < hop_s: break
#print len(beats)


audio = play_song(filename)

audio.start()


beat_time_iterator = 0
time_threshold = 0.05

beat_counter = 0

iterator_offset = 0#4

print(beat_times)

print(len(beat_times))

while True:
    if beat_time_iterator < len(beat_times) + iterator_offset:
        # print(audio.current_time())
        while beat_times[beat_time_iterator] < audio.current_time() - time_threshold*2:
            print('catching up')
            beat_time_iterator = beat_time_iterator + 1


        # if beat_time_iterator > iterator_offset:
        #     print(audio.current_time())
        #     print(beat_times[beat_time_iterator - iterator_offset])


        # print(abs(beat_times[beat_time_iterator - iterator_offset] - audio.current_time()))

        # if abs(beat_times[beat_time_iterator - iterator_offset] - audio.current_time()) < time_threshold:
        #     print('a')


        if beat_time_iterator > iterator_offset and \
                        abs(beat_times[beat_time_iterator - iterator_offset] - audio.current_time()) < time_threshold:
            print('BEAT %d' % beat_counter)
            beat_counter = beat_counter + 1
            beat_time_iterator = beat_time_iterator + 1
        # elif beat_times[beat_time_iterator] < audio.current_time() - time_threshold:
        #     beat_time_iterator = beat_time_iterator + 1


        time.sleep(0.0001)
    else:
        break


audio.stop()

