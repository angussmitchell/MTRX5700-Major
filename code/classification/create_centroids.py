import numpy as np
from sklearn.decomposition import PCA

sparse = np.loadtxt("sparse/sparse.txt")
chorus = np.loadtxt("chorus/chorus.txt")


## Perform PCA on chorus
pca = PCA(2)
pca.fit(chorus)
chorus = pca.transform(chorus)

## Perform PCA on sparse
pca = PCA(2)
pca.fit(sparse)
spar = pca.transform(sparse)

#calcualte typical spare section
sparse = np.transpose(np.average(sparse, axis = 0))
chorus = np.transpose(np.average(chorus, axis = 0))



np.savetxt("sparse/typical_sparse.txt",sparse)
np.savetxt("chorus/typical_chorus.txt",chorus)
