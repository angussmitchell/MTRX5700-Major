
import time
from play_song import play_song
from cluster import cluster
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt

filename = '../music/actionclip.wav'

rate, raw_data = wavfile.read(filename)
data = (raw_data[:, 0] / 2.0 + raw_data[:, 1] / 2.0)

# get mfcc todo use cluster labels
time_song, labels, class_labels = cluster(data, samplerate=44100, show_plots=True)


data = data[1::10]
x = range(0, len(data))
#plot the song
plt.subplot(311)
plt.scatter(time_song, labels)
plt.grid(which='major', alpha=0.5)
plt.grid(which='minor', alpha=0.5)

plt.axis([0, max(time_song), min(labels),max(labels) ])

plt.subplot(312)
plt.scatter(time_song, class_labels)
plt.ylabel('amplitude')
plt.xlabel('sample No.')
plt.title('raw .WAV data')
plt.grid(which='major', alpha=0.5)
plt.grid(which='minor', alpha=0.5)
plt.axis([0, max(time_song), min(labels),max(labels) ])

plt.subplot(313)
plt.plot(x, data)
plt.grid(which='major', alpha=0.5)
plt.grid(which='minor', alpha=0.5)
plt.axis([0, max(x), min(data), max(data)])


plt.show()