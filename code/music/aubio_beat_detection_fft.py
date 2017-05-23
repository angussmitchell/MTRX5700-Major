#! /usr/bin/env python
## in this file, i'll try to do sound file segmentation - i.e. determine if a bar is in a certain
import aubio
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
import numpy as np
import numpy.fft as fft
from scikits.talkbox.features import mfcc

#close all figs
plt.close("all")

#parameters for reading the wav file
win_s = 512                 # fft size
hop_s = win_s // 2          # hop size
filename = 'nothing.wav'
samplerate = 0

#read the wav file for processing
s = aubio.source(filename, samplerate, hop_s)
samplerate = s.samplerate
o = aubio.tempo("default", win_s, hop_s, samplerate)

# tempo detection delay, in samples
# default to 4 blocks delay to catch up with
delay = 4. * hop_s

# list of beats, in samples
beats = []


#read in all the beats
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


# import song for display
rate, raw_data = wavfile.read(filename)

#merge raw data channels
mono_data = (raw_data[:,0] + raw_data[:,1]) /3

#as a test, calculate FFT of first bar (from beat 1 to beat 2)
bar = mono_data[beats[70]:beats[71]]
fft = fft.rfft(bar)
fft = abs(fft)
ceps, mspec, spec = mfcc(bar,len(bar),len(bar),samplerate,40)


#find overall BPM
BPM_list = [j-i for i, j in zip(beats[:-1], beats[1:])]    #find differentes between each element using zip
T_samples = np.average(BPM_list)                            #average out differences
T_seconds = float(T_samples/samplerate)                     # convert to period in seconds
BPM = (1/T_seconds)*60                                      #convert to BPM

## PLOTTING
plt.figure(1)
plt.subplot(311)
plt.plot(bar,'ro',)
plt.ylabel('amplitude')
plt.xlabel('sample No.')
plt.title('first bar BPM = %d' % BPM)

plt.subplot(312)
plt.plot(fft,'ro',)
plt.ylabel('')
plt.xlabel('')
plt.title('fft')

plt.subplot(313)
plt.plot(np.transpose(ceps),'ro')
plt.ylabel('')
plt.xlabel('')
plt.title('fft')
plt.show()


