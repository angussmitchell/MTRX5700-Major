import scipy.io.wavfile as wavfile
import numpy as np
import matplotlib.pyplot as plt
from scikits.talkbox.features import mfcc
import numpy.fft as fft
from sklearn.decomposition import PCA
from sklearn.cluster import MeanShift, estimate_bandwidth
from mpl_toolkits.mplot3d import Axes3D
from itertools import cycle

def cluster(data,samplerate = 44100):
    ## set up parameter
    num_features = 2
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
    pca = PCA(num_features)
    pca.fit(features)
    features = pca.transform(features)
    time = np.arange(0, num_chunks,dtype=float)*chunk_size / samplerate

    ##before we plot the features, we should sub sample to make plotting easier
    # x1 = features[:,0]
    # sub_x1 = x1[1::4]
    # x2 = features[:, 1]
    # sub_x2 = x2[1::4]
    # sub_time = time[1::4]
    #
    #
    # # the following plots the feature space for manual cluster detection
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(sub_x1,sub_x2,sub_time)
    # plt.show()

    # Do MeanShift clustering
    bandwidth = estimate_bandwidth(features, quantile=0.1, n_samples=num_chunks)
    ms = MeanShift(bandwidth = bandwidth, bin_seeding=True,cluster_all = False,n_jobs = -1, min_bin_freq= 50)     #setup MeanShift parameters
    ms.fit(features)                                        #fit MeanShift to data
    labels = ms.labels_                                         #collect cluster labels
    cluster_centers = ms.cluster_centers_                       #record cluster centers
    unique_labels = np.unique(labels)                           #get unique clusters
    n_clusters = len(unique_labels)                            #get the number of unique clusters

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #plotting - a different colour for every cluster
    # colours = "rgbyk"
    # for k in range(0,n_clusters):
    #     my_members = labels == k
    #     colour_index = k%len(colours)
    #     ax.scatter(features[my_members,0], features[my_members,1],time[my_members], c = colours[colour_index])
    #     #plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=14)
    # plt.title('Calculate number of clusters = : %d' % n_clusters)
    # plt.show()


    return 0
    #now we have features, we should get clusters

