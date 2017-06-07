import numpy as np

#load in features
sparse_features = np.loadtxt("sparse/sparse.txt")
chorus_features = np.loadtxt("chorus/chorus.txt")

num_sparse_features = len(sparse_features[:,0])
num_chorus_features = len(chorus_features[:,0])
num_total_features = num_sparse_features+ num_chorus_features
#create label array
sparse_labels = np.zeros([num_sparse_features,1])
chorus_labels = np.ones([num_chorus_features,1])

#combine datasets
labels = np.concatenate((sparse_labels,chorus_labels), axis = 0)
features = np.concatenate((sparse_features,chorus_features), axis = 0)

#combine features and lables
features = np.concatenate((features,labels),axis = 1)

#shuffle features
np.random.shuffle(features)

#save 20% for test set 20% for validation set
num_test_set = int(0.2*num_total_features)
num_val_set = int(0.2*num_total_features)
test_set = features[0:num_test_set,0:41]
val_set = features[num_test_set:num_test_set +num_val_set, 0:41]
train_set = features[num_test_set +num_val_set :num_total_features,0:41]

#save these sets
np.savetxt("NN_data/train_set",train_set)
np.savetxt("NN_data/test_set",test_set)
np.savetxt("NN_data/val_set",val_set)


