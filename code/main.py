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
import os

## implement later when we have live music working
#live = False
#if live == True         # check if we want the drone to dance to live music
#    import liveMusic
#else:
#    import recordedMusic


## do music processing first

# beat detection variables
filename = 'Angels.wav'
win_s = 512             # fft size
delay_b = 4             # tempo detection delay (blocks)

samplerate, beats = get_beats(filename, win_s, delay_b)  # get the detected beats (samples)

beat_times = beats/float(samplerate)    # convert beats (samples) to beats (seconds)
dt = [j-i for i, j in zip(beat_times[:-1], beat_times[1:])] # array of times between each beat (seconds)
dt = np.asarray(dt,dtype = float)

## control drone based on sequence
drone = drone_presets.clean_start()

#####################################################
#                 MAIN LOOP                         #
#####################################################
#play song
command_str = 'play ' + filename + ' &'
os.system(command_str)  #play sound asyncronously (i.e. in the background)

time.sleep(beats[0]/44100.0) #wait till first beat catches up

# for i in range(0,40,2):
#
#     #alternate between 'dance moves'
#     if i%4:
#         drone.relMove(0,0,0,1)    #all leds are red
#         print("left!")
#     else:
#         drone.relMove(0,0,0,-1)   #all leds ardrone = ps_drone.Dronee green
#         print("right!")
#
#     time.sleep(dt[i]+dt[i+1])  #sleep for the time between beats
#
#
# #do a flip to end it
# drone.anim(18,5)
# print("backflip!")

# drone.turnAngle(179.9, 0.7)
# drone.turnAngle(-179.9, 0.7)

drone.land()        #finish program, land drone
command_str = 'kill %1'
os.system(command_str)  #kill backgroun process


drone.doggyWag()
