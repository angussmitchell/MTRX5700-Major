#! /usr/bin/env python
import aubio
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
import numpy as np

#close all figs
plt.close("all")

win_s = 512                 # fft size
hop_s = win_s // 2          # hop size

filename = 'faster.wav'

samplerate = 0

s = aubio.source(filename, samplerate, hop_s)
samplerate = s.samplerate
o = aubio.tempo("default", win_s, hop_s, samplerate)

# tempo detection delay, in samples
# default to 4 blocks delay to catch up with
delay = 4. * hop_s

# list of beats, in samples
beats = []



# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    is_beat = o(samples)
    if is_beat:
        this_beat = int(total_frames - delay + is_beat[0] * hop_s)
        #print("%f" % (this_beat / float(samplerate)))
        beats.append(this_beat)
    total_frames += read
    if read < hop_s: break


# import song
rate, raw_data = wavfile.read("faster.wav")

#produce a sin wave
Fs = 44100
f = 261.1
amp = 15000
samples = len(raw_data)
x = np.arange(samples)
y = amp*np.sin(np.pi * f * x / Fs)

#plt.plot(x[0:5000],y[0:5000],'ro')
#plt.show()

#mask array
mask = np.zeros(samples)
buzz_len = 5512
for x in range(0,len(beats)-2):

    #fig = plt.figure()
    pos_min = beats[x] - buzz_len/2
    pos_max = beats[x] + buzz_len/2
    mask[pos_min:pos_max] = np.ones(buzz_len)

## create sin mask
sin_mask = np.vectorize(mask * y)   #convert list to array
sin_mask = int(sin_mask)            #convert float array to int array

#plt.plot(sin_mask[beats[0]-5000:beats[5]+5000],'ro')
#plt.show()

#merge raw data channels
# mono_data = int(raw_data.sum(axis=1)/2) + np.zeros(len(raw_data))
mono_data = int(raw_data.sum(axis=1)/2)

#put the buzz in the song
buzzed_data = mono_data + sin_mask

wavfile.write('faster_processed.wav',44100,mono_data)
#plotting
zeros = np.zeros(len(beats))
plt.plot(buzzed_data[0:len(raw_data)/10],'ro',)
plt.ylabel('amplitude')
plt.xlabel('sample No.')
plt.title('raw .WAV data')
plt.show()