#! /usr/bin/env python
import aubio
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
import numpy as np

#close all figs
plt.close("all")

win_s = 512                 # fft size
hop_s = win_s // 2          # hop size

filename = 'nothing.wav'

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
rate, raw_data = wavfile.read(filename)

#produce a sin wave
Fs = 44100
f = 1000
amp = 15000
samples = len(raw_data)
x = np.arange(samples)
y = amp*np.sin(np.pi * f * x / Fs)

#plt.plot(x[0:5000],y[0:5000],'ro')
#plt.show()

#mask array
mask = np.zeros(samples)
buzz_len = 1000
for x in range(0,len(beats)-2):

    #fig = plt.figure()
    pos_min = beats[x]
    pos_max = beats[x] + buzz_len
    mask[pos_min:pos_max] = np.ones(buzz_len)

## create sin mask
sin_mask = mask * y
sin_mask = sin_mask.astype(np.int16)
#plt.plot(sin_mask[beats[0]-5000:beats[5]+5000],'ro')
#plt.show()

#merge raw data channels
mono_data = (raw_data[:,0] + raw_data[:,1]) /3


#put the buzz in the song
buzzed_data = mono_data + sin_mask
wavfile.write('processed.wav',44100,buzzed_data)


#find overall BPM
BPM_list = [j-i for i, j in zip(beats[:-1], beats[1:])]    #find differentes between each element using zip
T_samples = np.average(BPM_list)                            #average out differences
T_seconds = float(T_samples/samplerate)                     # convert to period in seconds
BPM = (1/T_seconds)*60                                      #convert to BPM

##plotting
zeros = np.zeros(len(beats))
plt.plot(buzzed_data[0:len(buzzed_data)/10],'ro',)
plt.ylabel('amplitude')
plt.xlabel('sample No.')
plt.title('raw .WAV data BPM = %d' % BPM)
plt.show()

