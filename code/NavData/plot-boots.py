## MTRX5700
# Xue Yin Zhang
#
# Dependencies: check init_boots.py to see which data packages have been enabled/saved
#
# Note to Neill: check battery status before each move

from numpy import *
import math
import matplotlib.pyplot as plt
#import pylab as plt
import pickle

with open('navdata-vars.pickle') as f:  # Python 3: open(..., 'rb')
#    pitch, roll, yaw, demo_alt, vx, vy, vz, nav_time, magneto, magneto_raw, pwm_fl, pwm_fr, pwm_br, pwm_bl, detect_n, detect_type, detect_x, detect_y, detect_width, detect_depth, detect_dist, detect_ang, detect_rot, checksum = pickle.load(f)
    pitch, roll, yaw, vx, vy, vz, nav_time, mx, my, mz, altitude_ref, detect_n, detect_rot = pickle.load(f)

## calculating the time
x = [y - nav_time[0] for y in nav_time]

## marker plots
plt.figure(1)

plt.subplot(311)
plt.plot(x, detect_n,'r', label = "number of detected markers")
plt.legend(loc='upper right')
plt.grid(True)
plt.xlabel("Time (s)")

plt.subplot(312)
plt.plot(x, detect_rot,'g', label = "rotation")
plt.legend(loc='upper right')
plt.grid(True)
plt.xlabel("Time (s)")

plt.subplot(313)
plt.plot(x, detect_dist,'b', label = "distance from marker")
plt.legend(loc='upper right')
plt.grid(True)
plt.xlabel("Time (s)")

plt.title("Oriented Marker Detections")
plt.xlabel("Time (s)")

## altitude plots
plt.figure(2)

plt.plot(x, altitude_ref,'g', label = "altitude (altitude ref)")
plt.legend(loc='upper right')
plt.grid(True)
plt.xlabel("Time (s)")
plt.title("Altitude Measurements")
plt.xlabel("Time (s)")

plt.show()

##


#print "show number of markers"
#for p in detect_n: print p
