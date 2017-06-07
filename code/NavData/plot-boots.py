## MTRX5700
# Xue Yin Zhang
#
# Dependencies: check init_boots.py to see which data packages have been enabled
#
# Note to Neill: check battery status before each move

from numpy import *
import math
import matplotlib.pyplot as plt

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

fh = open("NavData-6Jun-good.txt", "r")
data = fh.readlines()

pitch = []
roll = []
yaw = []
alt = []
sens = []
pres = []
magx = []
magy = []
magz = []

with open("NavData-6Jun-good.txt", "r") as f:
    for line in f:
        if 'Aptitude' in line:  # extract on the data values for aptitude (pitch roll yaw)
#            print "Apt: " + line[31:-2]
            ind = find(line, ",")
            pitch.append(line[31:ind[2]])
            roll.append(line[ind[2]+1:ind[3]])
            yaw.append(line[ind[3]+1:-2])
#            print pitch[-1] + " " + roll[-1] + " " + yaw[-1]
        elif 'Altitude' in line:
#            print "Alt: " + line[30:-2]
            ind = find(line, "/")
            alt.append(line[30:ind[2]-1])
            sens.append(line[ind[2]+2:ind[3]-1])
            pres.append(line[ind[3]+2:])
        elif 'Megnetometer' in line:
            ind = find(line, ",")
            magx.append(line[31:ind[2]])
            magy.append(line[ind[2]+1:ind[3]])
            magz.append(line[ind[3]+1:-2])
#            print "Mag: " + line[31:-2]



plt.plot(pitch,'r') # plotting t,a separately
plt.plot(roll,'b') # plotting t,b separately
plt.plot(yaw,'g') # plotting t,c separately

plt.show()
