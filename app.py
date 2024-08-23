import tensorflow as tf
from tensorflow.keras import datasets, layers, models
# import matplotlib.pyplot as plt
# import numpy as np

(X_train, Y_train), (X_test, Y_test) = datasets.cifar10.load_data()

print(X_train.shape)