import scipy.io.wavfile as wavfile
import numpy as np
import matplotlib.pyplot as plt
from scikits.talkbox.features import mfcc
import numpy.fft as fft
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from mpl_toolkits.mplot3d import Axes3D
from itertools import cycle

def cluster(data,samplerate = 44100,num_coeficients = 40):
    ## set up parameter
    num_features = 2
    chunk_size = 1024*2
    min_bin_freq = 1     #minimum number of samples to form a cluster
    print "cluster chunk size = " + str(float(chunk_size/samplerate)) + " seconds"
    num_chunks = len(data)/chunk_size-1
    ceps = []
    features = np.zeros((num_chunks, num_coeficients))
    quantile = 0.99       #determines the filter bandwidth

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
    num_samples = len(features[:,0])
    time = np.arange(0, num_samples,dtype=float)*chunk_size / samplerate
    time = np.transpose(np.asarray(time)) * 50
    ##before we plot the features, we should sub sample to make plotting easier
    #
    #
    # # the following plots the feature space for manual cluster detection
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(sub_x1,sub_x2,sub_time)
    # plt.show()


    #add time into the feature list, because it is an important feature
    combined_features = np.empty([num_samples, 3], dtype = float)
    combined_features[:,0] = features[:,0]
    combined_features[:,1] = features[:,1]
    combined_features[:,2] = time
    features = combined_features

    db = DBSCAN(eps=5000, min_samples=1).fit(features)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    print  str(n_clusters) + " clusters found"
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #plotting - a different colour for every cluster
    colours = "rgbyk"
    for k in range(0,n_clusters):
         my_members = labels == k
         colour_index = k%len(colours)
         ax.scatter(features[my_members,0], features[my_members,1],time[my_members], c = colours[colour_index])
         #plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=14)
    plt.title('Calculate number of clusters = : %d' % n_clusters)
    plt.show()



    return time, labels
    #now we have features, we should get clusters

