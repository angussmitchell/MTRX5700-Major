### MTRX5700
# Dancing Drone
# Angus, Neill, Xue Yin
#
# main.py
#  - combines the drone preset moves module with the music processing module

# import subprocess
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
from drone_dancer import drone_dancer

# dancer = drone_dancer()

## implement later when we have live music working
#live = False
#if live == True         # check if we want the drone to dance to live music
#    import liveMusic
#else:
#    import recordedMusic


## do music processing first

# beat detection variables
filename = 'FasterFurther.wav'
win_s = 512             # fft size
delay_b = 4             # tempo detection delay (blocks)

samplerate, beats = get_beats('./music/' + filename, win_s, delay_b)  # get the detected beats (samples)

beat_times = beats/float(samplerate)    # convert beats (samples) to beats (seconds)
dt = [j-i for i, j in zip(beat_times[:-1], beat_times[1:])] # array of times between each beat (seconds)
dt = np.asarray(dt,dtype = float)

## control drone based on sequence
# drone = drone_presets.clean_start()

#####################################################
#                 MAIN LOOP                         #
#####################################################
#play song
command_str = './music/playsong.sh ' + './music/' + filename + ' &>/dev/null'
print(command_str)
os.system(command_str)  #play sound asyncronously (i.e. in the background)


# time.sleep(beats[0]/float(samplerate)) #wait till first beat catches up

for i in range(0, 300, 1):
    print('beat ' + str(i))
    print('dt ' + str(dt[i]))
    print('current bpm: ' + str(1.0/dt[i] * 60))
    time.sleep(dt[i])
#
#     sleeptime = 1.0 / (163.0 / 60)
#
#     if(i == 55):
#         dancer.takeoff(True)
#         dancer.drone.moveUp(1)
#         time.sleep(1)
#         dancer.drone.hover()
#
#     if(i == 55):
#         dancer.do_move(dancer.dance_moves.MOVE_FLIP)
#
#     if i > 55:
#         dancer.do_move(dancer.dance_moves.MOVE_WIGGLE_TOGGLE)
#         time.sleep(sleeptime/2)
#         dancer.do_move(dancer.dance_moves.MOVE_WIGGLE_TOGGLE)
#         time.sleep(sleeptime/2)
#     else:
#         time.sleep(sleeptime)

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




# drone.turnAngle(179.9, 0.7)
# drone.turnAngle(-179.9, 0.7)
time.sleep(1)
# drone.land()        #finish program, land drone
command_str = './music/stopsong.sh'
os.system(command_str)  #kill backgroun process


# drone.doggyWag()
