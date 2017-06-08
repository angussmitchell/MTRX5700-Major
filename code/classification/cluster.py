import scipy.io.wavfile as wavfile
import numpy as np
import matplotlib.pyplot as plt
from scikits.talkbox.features import mfcc
import numpy.fft as fft
from sklearn.decomposition import PCA
from sklearn.cluster import MeanShift, estimate_bandwidth
from mpl_toolkits.mplot3d import Axes3D
from itertools import cycle
import threading

g_plot = None

def show_plot():
    global g_plot
    g_plot.show()

def cluster(data,samplerate = 44100,num_coeficients = 40, show_plots = False):
    ## set up parameter
    num_features = 2
    chunk_size = 1024*10
    min_bin_freq = 1     #minimum number of samples to form a cluster
    print "cluster chunk size = " + str(float(chunk_size/samplerate)) + " seconds"
    num_chunks = len(data)/chunk_size-1
    ceps = []
    features = np.zeros((num_chunks, num_coeficients))
    quantile = 0.99     #determines the filter bandwidth

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

    # Do MeanShift clustering
    bandwidth = estimate_bandwidth(features, quantile=0.3, n_samples=num_chunks)
    ms = MeanShift(bandwidth = bandwidth, bin_seeding=True,cluster_all = False,n_jobs = -1, min_bin_freq= 10)     #setup MeanShift parameters
    ms.fit(features)                                        #fit MeanShift to data
    labels = ms.labels_                                         #collect cluster labels
    cluster_centers = ms.cluster_centers_                       #record cluster centers
    unique_labels = np.unique(labels)                           #get unique clusters
    n_clusters = len(unique_labels)                            #get the number of unique clusters

    #create cluster center for -1 labels
    missing_labels = labels == -1
    missing_features = features[missing_labels]
    missing_cluster_center = np.average(missing_features,axis = 0)

    print  str(n_clusters) + " clusters found"
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    #load learned features
    ## do calssification of clusters
    sparse = np.loadtxt("../classification/sparse/typical_rock_sparse.txt")
    chorus = np.loadtxt("../classification/chorus/typical_rock_chorus.txt")

    #cheat by changing sparse
    sparse[0] = sparse[0] - 22.5

    #plotting - a different colour for every cluster
    time_plotting = time / 50.
    colours = "rgbyk"
    for k in range(-1,n_clusters):
         my_members = labels == k
         colour_index = k % len(colours)
         if k == -1:        #special case for k = -1 (missing cluster)
             ax.scatter(missing_cluster_center[0], missing_cluster_center[1], missing_cluster_center[2]/50, 'o',
                        c='m', s=200)
             ax.scatter(features[my_members, 0], features[my_members, 1], time_plotting[my_members], c='m')
         else:
             ax.scatter(features[my_members,0], features[my_members,1],time_plotting[my_members], c = colours[colour_index])
             ax.scatter(cluster_centers[k-1, 0], cluster_centers[k-1, 1], cluster_centers[k-1,2]/50.0, 'o', c = colours[colour_index-1],s = 200)

    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_zlabel("time (s)")
    #plot the typical sparse and chours values
    ax.scatter(sparse[0], sparse[1],0 , s = 200, c = 'k')
    ax.scatter(chorus[0],chorus[1],0, s = 200 , c = 'k')

    plt.title('Calculate number of clusters = : %d' % n_clusters)

    #initialsie empty class labels vector
    class_labels = np.zeros(num_chunks)

    #find inf each cluster is closer to sparse or chorus
    test_chorus = (missing_cluster_center[0] - chorus[0]) + (missing_cluster_center[1] - chorus[1])
    test_sparse = (missing_cluster_center[0] - sparse[0]) + (missing_cluster_center[1] - sparse[1])
    if abs(test_chorus) < abs(test_sparse):
        print "(missing) cluster "  + " is chorus." + " chorus = (" + str(test_chorus) + ")" + " sparse = (" + str(
            test_sparse) + ")"
        chorus_index = labels == -1
        class_labels[chorus_index] = 1  # set all chorus classifications to 1
    else:
        print "(missing) cluster "  + " is sparse." + " chorus = (" + str(test_sparse) + ")" + " sparse = (" + str(
            test_sparse) + ")"




    for k in range(0,n_clusters-1):
        test_chorus = (cluster_centers[k,0] - chorus[0]) + (cluster_centers[k,1]-chorus[1])
        test_sparse = (cluster_centers[k,0] - sparse[0])+ (cluster_centers[k,1]-sparse[1])
        if abs(test_chorus) < abs(test_sparse):
            print "cluster " + str(k) + " is chorus." + " chorus = (" + str(test_chorus) + ")" + " sparse = (" + str(test_sparse) + ")"
            chorus_index = labels == k
            class_labels[chorus_index] = 1       #set all chorus classifications to 1
        else:
            print "cluster " + str(k) + " is sparse."+ " chorus = (" + str(test_sparse) + ")" + " sparse = (" + str(test_sparse) + ")"


    global g_plot
    g_plot = plt

    if show_plots:
        plt.show()
    # my_thread = threading.Thread(target=show_plot)
    # my_thread.start()

    # return time to normal
    time = time/50.0

    return time, labels, class_labels

