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
    pitch, roll, yaw, demo_alt, vx, vy, vz, nav_time, magneto, magneto_raw, pwm_fl, pwm_fr, pwm_br, pwm_bl, detect_n, detect_type, detect_x, detect_y, detect_width, detect_depth, detect_dist, detect_ang, detect_rot, checksum = pickle.load(f)

#plt.plot(pitch,'r') # plotting t,a separately
#plt.plot(roll,'b') # plotting t,b separately
#plt.plot(yaw,'g') # plotting t,c separately
#
#plt.show()

"""
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
plt.xlabel("Package number")
plt.show()
"""

##


#print "show number of markers"
#for p in detect_n: print p
