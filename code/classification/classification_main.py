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
rate, raw_data = wavfile.read("../music/Vegas.wav")
data = (raw_data[:,0]/2.0+raw_data[:,1]/2.0)

#cluster(data[0:1024*10])
# get mfcc
time, labels, class_labels = cluster(data,samplerate=44100, show_plots=True)


data = data[1::10]
x = range(0, len(data))
#plot the song
plt.subplot(311)
plt.scatter(time, labels)
plt.grid()
plt.axis([0, max(time), min(labels),max(labels) ])

plt.subplot(312)
plt.scatter(time, class_labels)
plt.ylabel('amplitude')
plt.xlabel('sample No.')
plt.title('raw .WAV data')
plt.grid()
plt.axis([0, max(time), min(labels),max(labels) ])

plt.subplot(313)
plt.plot(x, data)
plt.grid()
plt.axis([0, max(x), min(data), max(data)])

plt.show()

