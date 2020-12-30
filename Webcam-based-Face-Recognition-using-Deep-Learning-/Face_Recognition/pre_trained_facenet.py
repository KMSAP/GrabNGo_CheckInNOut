
import os
import tensorflow as tf
from tensorflow.python.framework import ops
import numpy as np
from tensorflow.python.training import training
from tensorflow.python.platform import gfile


def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1/std_adj)
    return y  

def load_model(model):
    # Check if the model is a model directory (containing a metagraph and a checkpoint file)
    #  or if it is a protobuf file with a frozen graph
    model_exp = os.path.expanduser(model)
    if (os.path.isfile(model_exp)):
        print('Model filename: %s' % model_exp)
        with gfile.FastGFile(model_exp,'rb') as f:
            # graph_def = tf.GraphDef() #for TF1.0
            graph_def = tf.compat.v1.GraphDef() #replacement
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')
    else:
        print('no pre-trained data')
    