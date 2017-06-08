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
    pitch, roll, yaw, demo_alt, vx, vy, vz, nav_time, mx, my, mz, detect_n, detect_dist, detect_rot = pickle.load(f)

## plot the pwm data
x = [y - nav_time[0] for y in nav_time]
#nav_time[0]
#nav_time[0] - 1
plt.figure(1)

plt.subplot(211)
plt.plot(x, pwm_fl,'r', label = "front left")
plt.plot(x, pwm_fr,'g', label = "front right")
plt.plot(x, pwm_br,'b', label = "back right")
plt.plot(x, pwm_bl,'c', label = "back left")
plt.legend(loc='upper right')
plt.grid(True)
plt.title("Motor PWM values")
plt.ylabel("Motor PWMs")
plt.xlabel("Time (s)")

plt.subplot(212)
plt.plot(x, pitch,'r', label = "pitch")
plt.plot(x, roll,'g', label = "roll")
plt.plot(x, yaw,'b', label = "yaw")
plt.legend(loc='upper right')
plt.grid(True)
plt.title("Accelerometer values")
plt.ylabel("Angle")
plt.xlabel("Time (s)")

plt.show()

plt.figure(2)
plt.plot(x, detect_n)

plt.show()

##


#print "show number of markers"
#for p in detect_n: print p
