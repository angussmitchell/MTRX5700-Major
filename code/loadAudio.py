import scipy.io.wavfile as wavfile
import numpy as np
import matplotlib.pyplot as plt

rate, raw_data = wavfile.read("music/rome.wav")

raw_data = (raw_data[:,0]+raw_data[:,1])/2
windowSize = 30            # 2 minutes
window = rate*windowSize     #how many samples we need to get a window


plt.plot(raw_data[0:window],'r')
plt.ylabel('amplitude')
plt.xlabel('sample No.')
plt.title('raw .WAV data')
plt.axis([0, 3000000, -60000, 60000])


# implement sound energy beat detection algorithm
maxBpm = 180
maxSamples = ((maxBpm/60)*rate)/10    #this is how many samples we look at to find noise hsitory
threshold = 500000
obsSpace = 1024
instant_pow = 0
i = 1024 + maxSamples

while i < window-maxSamples:  #start with enough samples to take noise history
    instant_pow = np.sum(abs(raw_data[i:i+1024]))    #find the 'instant' power over the 1024 elements
    surrounding_pow = np.sum(abs(raw_data[(i-maxSamples/2):(i-1)]))+ np.sum(abs(raw_data[(i+1):(i+maxSamples/2)])) #find the surrounding power

    print(i)
    if instant_pow +threshold > surrounding_pow & instant_pow > 20000:
        plt.plot([i, i], [-60000, 60000], color='k', linestyle='-', linewidth=2)
        print "beat detected", i
        i = i + maxSamples

    i = i + 10






print("looping done")
plt.show()
print('hello world')