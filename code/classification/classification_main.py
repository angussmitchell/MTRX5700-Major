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
time, labels = cluster(data,samplerate=44100)


data = data[1::10]
x = range(0, len(data))
 #plot the song
plt.subplot(211)
plt.scatter(time, labels)
plt.ylabel('amplitude')
plt.xlabel('sample No.')
plt.title('raw .WAV data')
plt.grid()
plt.axis([0, max(time), min(labels),max(labels) ])
plt.subplot(212)
plt.plot(x, data)
plt.grid()
plt.axis([0, max(x), min(data), max(data)])
plt.show()

