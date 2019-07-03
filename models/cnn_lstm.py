from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from models.custom_layers import bidirectional_lstm, batch_stat


class ConvLSTM(object):
    def __init__(self, num_classes, cnn_kernel_size=30,
                 pool_size=15, pool_stride=15, lstm_dim=1024,
                 max_len=100):
        self.num_classes = num_classes
        self.cnn_kernel_size = cnn_kernel_size
        self.pool_size = pool_size
        self.pool_stride = pool_stride
        self.lstm_dim = lstm_dim
        self.max_len = max_len

    def __call__(self, inputs):
        inputs = tf.reshape(inputs, [-1, self.max_len, 4])
        inputs = tf.layers.conv1d(inputs=inputs, filters=1024,
                                  kernel_size=self.cnn_kernel_size,
                                  padding='valid', activation=tf.nn.relu)
        inputs = tf.layers.max_pooling1d(inputs=inputs, pool_size=self.pool_size,
                                         strides=self.pool_stride, padding='valid')
        length_list, length_max, batch_size = batch_stat(inputs)
        inputs = bidirectional_lstm(inputs, self.lstm_dim, length_list, batch_size,
                                    initializer=tf.contrib.layers.xavier_initializer())
        inputs = tf.nn.tanh(inputs)
        inputs = tf.layers.flatten(inputs)
        inputs = tf.layers.dense(inputs=inputs, units=1024, activation=tf.nn.relu)
        inputs = tf.layers.dense(inputs=inputs, units=512, activation=tf.nn.relu)
        logits = tf.layers.dense(inputs=inputs, units=self.num_classes, activation=None)

        return logits


class Conv2LSTM(object):
    def __init__(self, num_classes, cnn_kernel_size=26,
                 pool_size=13, pool_stride=13, lstm_dim_1=320,
                 lstm_dim_2=640, max_len=100):
        self.num_classes = num_classes
        self.cnn_kernel_size = cnn_kernel_size
        self.pool_size = pool_size
        self.pool_stride = pool_stride
        self.lstm_dim_1 = lstm_dim_1
        self.lstm_dim_2 = lstm_dim_2
        self.max_len = max_len

    def __call__(self, inputs):
        inputs = tf.reshape(inputs, [-1, self.max_len, 4])
        inputs = tf.layers.conv1d(inputs=inputs, filters=320,
                                  kernel_size=self.cnn_kernel_size,
                                  padding='valid', activation=tf.nn.relu)
        inputs = tf.layers.max_pooling1d(inputs=inputs, pool_size=self.pool_size,
                                         strides=self.pool_stride, padding='valid')
        length_list, length_max, batch_size = batch_stat(inputs)
        with tf.variable_scope("lstm_1"):
            inputs = bidirectional_lstm(inputs, self.lstm_dim_1, length_list, batch_size,
                                        initializer=tf.contrib.layers.xavier_initializer())
            inputs = tf.nn.tanh(inputs)
        with tf.variable_scope("lstm_2"):
            inputs = bidirectional_lstm(inputs, self.lstm_dim_2, length_list, batch_size,
                                        initializer=tf.contrib.layers.xavier_initializer())
            inputs = tf.nn.tanh(inputs)
        inputs = tf.layers.flatten(inputs)
        inputs = tf.layers.dense(inputs=inputs, units=1024, activation=tf.nn.relu)
        inputs = tf.layers.dense(inputs=inputs, units=512, activation=tf.nn.relu)
        logits = tf.layers.dense(inputs=inputs, units=self.num_classes, activation=None)

        return logits

