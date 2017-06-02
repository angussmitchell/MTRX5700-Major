import scipy.io.wavfile as wavfile
import numpy as np
import matplotlib.pyplot as plt
from scikits.talkbox.features import mfcc
import numpy.fft as fft
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

def cluster(data,samplerate = 44100):
    ## set up parameter
    num_coeficients = 15
    chunk_size = 4096
    num_chunks = len(data)/chunk_size-1
    ceps = []
    features = np.zeros((num_chunks, num_coeficients))


    ## start finding MFCC for the song chunks
    for i in range(0,len(data)/chunk_size-1):
        index = i * chunk_size
        chunk = data[index:index + chunk_size]

        #ceps is the mel-cepstrum coefficients
        ceps, mspec, spec = mfcc(chunk, len(chunk), len(chunk), samplerate, num_coeficients)

        #save seps to feature vector
        ceps[np.isnan(ceps)] = 0
        ceps[np.isneginf(ceps)] = 0
        features[i] = ceps

    ## Perform PCA
    pca = PCA(2)
    pca.fit(features)
    features = pca.transform(features)
    time = np.arange(0, num_chunks,dtype=float)*chunk_size / samplerate

    #before we plot the features, we should sub sample to make plotting easier
    sub_x1 = features[:,0]
    sub_x1 = sub_x1[1::10]
    sub_x2 = features[:,1]
    sub_x2 = sub_x2[1::10]
    sub_time = time[1::10]

    ## the following plots the feature space for manual cluster detection
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(features[:,0],features[:,1],time)
    plt.show()

    ## means sift clustering



    return 0
    #now we have features, we should get clusters

