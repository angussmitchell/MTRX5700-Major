import scipy.io.wavfile as wavfile
import numpy as np
import matplotlib.pyplot as plt
from scikits.talkbox.features import mfcc
import numpy.fft as fft
from numpy import inf
from numpy import nan


def cluster(data,samplerate = 44100):

    num_coeficients = 15
    chunk_size = 1024
    ceps = []
    features = np.zeros((len(data)/chunk_size-1, num_coeficients))

    for i in range(0,len(data)/chunk_size-1):
        index = i * chunk_size
        chunk = data[index:index + chunk_size]

        #ceps is the mel-cepstrum coefficients
        ceps, mspec, spec = mfcc(chunk, len(chunk), len(chunk), samplerate, num_coeficients)

        #save seps to feature vector
        ceps[np.isnan(ceps)] = 0
        ceps[np.isneginf(ceps)] = 0
        features[i] = ceps

    return features
