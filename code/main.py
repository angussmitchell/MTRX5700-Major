### MTRX5700
# Dancing Drone
# Angus, Neill, Xue Yin
#
# main.py
#  - combines the drone preset moves module with the music processing module

import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
import time
import sys
import aubio
import ps_drone         # PS-drone API
import drone_presets    # import drone functions that we wrote
from recorded_music import get_beats  #import music processing functions

## implement later when we have live music working
#live = False
#if live == True         # check if we want the drone to dance to live music
#    import liveMusic
#else:
#    import recordedMusic
import recorded_music

## do music processing first

# beat detection variables
filename = 'music/Angels  Airwaves - It Hurts (Audio Video).wav'
win_s = 512             # fft size
delay_b = 4             # tempo detection delay (blocks)

samplerate, beats = get_beats(filename, win_s, delay_b)  # get the detected beats (samples)

beat_times = beats/float(samplerate)    # convert beats (samples) to beats (seconds)
dt = [j-i for i, j in zip(beat_times[:-1], beat_times[1:])] # array of times between each beat (seconds)

## control drone based on sequence
#drone = ps_drone.Drone
#drone = drone_presets.clean_Start()

#####################################################
#                 MAIN LOOP                         #
#####################################################
#play song

#wait till first beat catches up

for i in range(0,len(dt)):

    #alternate between 'dance moves'
    #if i%2:
    #    drone.led(7)    #all leds are red
    #else: drone.led(8)   #all leds are green

    time.sleep(dt)  #sleep for the time between beats




