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
from scikits.talkbox.features import mfcc
from sklearn.decomposition import PCA
from sklearn.cluster import MeanShift, estimate_bandwidth
from mpl_toolkits.mplot3d import Axes3D
from itertools import cycle
import glob

#takes some wav files and saves all their features in a huge feature array
def extract_features(path_to_files):

    features = np.empty([1,40])      #initialise feature vector

    #for every file in the glob, get mfcc
    for filename in glob.glob(path_to_files):

        # read in raw data
        rate, raw_data = wavfile.read("../music/Angles.wav")
        data = (raw_data[:, 0] / 2.0 + raw_data[:, 1] / 2.0)

        #initialise parameters
        chunk_size = 1024 * 20
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

    np.savetxt('mfcc_features.txt',features)
