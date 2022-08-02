from __future__ import absolute_import, division, print_function,unicode_literals

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow.compat.v2.feature_column as fc
import tensorflow as tf

# Basics
# string = tf.Variable("This is a string", tf.string)
# tf.rank()
# tf.reshape()
# shape attribute of every tensor
# tf.ones : filled with ones
# tf.zeroes: filled with zeros

# Linear Regression
dftrain = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/train.csv') #training data
dfevel = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/eval.csv') #testing data
y_train = dftrain.pop('survived')
y_eval = dfevel.pop('survived')


