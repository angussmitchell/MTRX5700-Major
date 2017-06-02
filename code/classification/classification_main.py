### MTRX5700
# Dancing Drone
# Angus, Neill, Xue Yin
#
#
# This file is a main file created for testing purposes, to get clustering and classification working
#

import scipy.io.wavfile as wavfile
import numpy as np
import matplotlib.pyplot as plt
from cluster import cluster

# read in raw data
rate, raw_data = wavfile.read("../music/Angles.wav")
data = (raw_data[:,0]/2.0+raw_data[:,1]/2.0)

# get mfcc
cluster(data,samplerate=44100)

# #plot the song
# plt.plot(raw_data,'r')
# plt.ylabel('amplitude')
# plt.xlabel('sample No.')
# plt.title('raw .WAV data')
# plt.axis([0, 9050000, -40000, 40000])
#plt.show()

