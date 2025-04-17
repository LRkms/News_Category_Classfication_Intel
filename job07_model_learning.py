import numpy as np
import matplotlib.pyplot as plt
from keras.models import *
from keras.layers import *

x_train = np.load('./crawling_data/title_x_train_wordszie15396.npy', allow_pickle=True)
x_test = np.load('./crawling_data/title_x_test_wordszie15396.npy', allow_pickle=True)
y_train = np.load('./crawling_data/title_y_train_wordszie15396.npy', allow_pickle=True)
y_test = np.load('./crawling_data/title_y_test_wordszie15396.npy', allow_pickle=True)
print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)