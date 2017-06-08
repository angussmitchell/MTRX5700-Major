import numpy as np
from scikits.talkbox.features import mfcc
from sklearn.decomposition import PCA

def cluster(chunk):
    samplerate = 44100
    num_coeficients = 40

    #get mfcc
    features, mspec, spec = mfcc(chunk, len(chunk), len(chunk), samplerate, num_coeficients)

    #do PCA
    pca = PCA(2)
    pca.fit(features)
    features = pca.transform(features)

    # load learned features
    ## do calssification of clusters
    sparse = np.loadtxt("./classification/sparse/typical_sparse.txt")
    chorus = np.loadtxt("./classification/chorus/typical_chorus.txt")

    test_chorus = (features[0] - chorus[0]) + (features[1] - chorus[1])
    test_sparse = (features[0] - sparse[0]) + (features[1] - sparse[1])

    if abs(test_chorus) > abs(test_sparse):
        print("chorus")
        return 1
    else:
        print("sparse")
        return 0

    

