import numpy as np
from sklearn.decomposition import PCA

sparse = np.loadtxt("rock_chill/rock_chill.txt")
chorus = np.loadtxt("rock_chorus/chorus.txt")

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



np.savetxt("sparse/typical_rock_sparse.txt",sparse)
np.savetxt("chorus/typical_rock_chorus.txt",chorus)
