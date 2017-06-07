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
from scikits.talkbox.features import mfcc



features = np.empty([1,40])      #initialise feature vector

# read in raw data
filename = input('enter file name: ')
filename_string = "../music/" + filename
rate, raw_data = wavfile.read(filename_string)
data = (raw_data[:, 0] / 2.0 + raw_data[:, 1] / 2.0)
start = int(input('start time (s)'))*rate
end = int(input('end time (s)'))*rate
data = data[start:end]

# plt.plot(data)
# plt.show()

#initialise parameters
chunk_size = 1024 * 10 #this equates to ~ 250ms
samplerate = 44100
num_coeficients = 40
num_chunks = len(data) / chunk_size - 1
local_features = np.zeros((num_chunks, num_coeficients))

#extract features from chunks
## start finding MFCC for the song chunks
for i in range(0, len(data) / chunk_size - 1):
    index = i * chunk_size
    chunk = data[index:index + chunk_size]

    # ceps is the mel-cepstrum coefficients
    ceps, mspec, spec = mfcc(chunk, len(chunk), len(chunk), samplerate, num_coeficients)

    # save seps to feature vector
    ceps[np.isnan(ceps)] = 0
    ceps[np.isneginf(ceps)] = 0
    local_features[i] = ceps

#append local_features to the final feature vector
features = np.concatenate((features,local_features),axis = 0)

#load other
loaded_features = np.loadtxt("chorus/chorus.txt")
features = np.concatenate((loaded_features,features),axis = 0)

output_folder = "chorus/"
output_filename = output_folder + "chorus.txt"
np.savetxt(output_filename,features)
