from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import tensorflow.contrib.slim as slim
from models.custom_layers import dense_block


class DeepCNN(object):
    def __init__(self, num_classes, max_len=100,
                 cnn_filter_size=(3, 3, 3, 3),
                 pooling_filter_size=(2, 2, 2, 2),
                 num_filters_per_size=(64, 128, 256, 512),
                 num_rep_block=(4, 4, 4, 4)):
        self.num_classes = num_classes
        self.max_len = max_len
        self.cnn_filter_size = cnn_filter_size
        self.pooling_filter_size = pooling_filter_size
        self.num_filters_per_size = num_filters_per_size
        self.num_rep_block = num_rep_block

    def __call__(self, inputs):
		# Modified from implementation by Hoa T. Le available at:
    	# https://github.com/lethienhoa/Very-Deep-Convolutional-Networks-for-Natural-Language-Processing
        inputs = tf.reshape(inputs, [-1, 4, self.max_len, 1])

        inputs = slim.conv2d(inputs=inputs,
                             num_outputs=self.num_filters_per_size[0],
                             kernel_size=[4, self.cnn_filter_size[0]],
                             weights_initializer=tf.contrib.layers.variance_scaling_initializer(
                                 factor=1.0, mode='FAN_AVG', uniform=True),
                             normalizer_fn=slim.batch_norm, scope='conv0', padding='SAME')

        for i in range(0, len(self.num_filters_per_size)):
            inputs = dense_block(inputs,
                                 self.num_filters_per_size[i],
                                 self.cnn_filter_size[i],
                                 self.num_rep_block[i])

            # Transition Layer
            if i != len(self.num_filters_per_size) - 1:
                inputs = slim.conv2d(inputs,
                                     self.num_filters_per_size[i + 1],
                                     [1, self.cnn_filter_size[i]],
                                     weights_initializer=tf.contrib.layers.variance_scaling_initializer(
                                         factor=1.0, mode='FAN_AVG', uniform=True),
                                     normalizer_fn=slim.batch_norm,
                                     scope='conv-last-%s' % i)

                # Max pooling 1/2
                inputs = slim.max_pool2d(inputs,
                                         [1, self.pooling_filter_size[i]],
                                         stride=self.pooling_filter_size[i],
                                         scope='pool_%s' % i)

        inputs = tf.nn.top_k(tf.transpose(inputs, [0, 1, 3, 2]), k=8, name='k_max_pool', sorted=False)[0]

        inputs = slim.flatten(inputs)
        inputs = slim.fully_connected(inputs, 2048, scope='FC1')
        inputs = slim.fully_connected(inputs, 2048, scope='FC2')
        logits = slim.fully_connected(inputs, self.num_classes, activation_fn=None, scope='output')

        return logits


class DeepCNN13(object):
    def __init__(self, num_classes, max_len=100,
                 cnn_filter_size=(3, 3, 3),
                 pooling_filter_size=(2, 2, 2),
                 num_filters_per_size=(64, 128, 256),
                 num_rep_block=(4, 4, 4)):
        self.num_classes = num_classes
        self.max_len = max_len
        self.cnn_filter_size = cnn_filter_size
        self.pooling_filter_size = pooling_filter_size
        self.num_filters_per_size = num_filters_per_size
        self.num_rep_block = num_rep_block

    def __call__(self, inputs):

        inputs = tf.reshape(inputs, [-1, 4, self.max_len, 1])

        inputs = slim.conv2d(inputs=inputs,
                             num_outputs=self.num_filters_per_size[0],
                             kernel_size=[4, self.cnn_filter_size[0]],
                             weights_initializer=tf.contrib.layers.variance_scaling_initializer(
                                 factor=1.0, mode='FAN_AVG', uniform=True),
                             normalizer_fn=slim.batch_norm, scope='conv0', padding='SAME')

        for i in range(0, len(self.num_filters_per_size)):
            inputs = dense_block(inputs,
                                 self.num_filters_per_size[i],
                                 self.cnn_filter_size[i],
                                 self.num_rep_block[i])

            # Transition Layer
            if i != len(self.num_filters_per_size) - 1:
                inputs = slim.conv2d(inputs,
                                     self.num_filters_per_size[i + 1],
                                     [1, self.cnn_filter_size[i]],
                                     weights_initializer=tf.contrib.layers.variance_scaling_initializer(
                                         factor=1.0, mode='FAN_AVG', uniform=True),
                                     normalizer_fn=slim.batch_norm,
                                     scope='conv-last-%s' % i)

                # Max pooling 1/2
                inputs = slim.max_pool2d(inputs,
                                         [1, self.pooling_filter_size[i]],
                                         stride=self.pooling_filter_size[i],
                                         scope='pool_%s' % i)

        inputs = tf.nn.top_k(tf.transpose(inputs, [0, 1, 3, 2]), k=8, name='k_max_pool', sorted=False)[0]

        inputs = slim.flatten(inputs)
        inputs = slim.fully_connected(inputs, 2048, scope='FC1')
        inputs = slim.fully_connected(inputs, 2048, scope='FC2')
        logits = slim.fully_connected(inputs, self.num_classes, activation_fn=None, scope='output')

        return logits


class DeepCNN9(object):
    def __init__(self, num_classes, max_len=100,
                 cnn_filter_size=(3, 3),
                 pooling_filter_size=(2, 2),
                 num_filters_per_size=(64, 128),
                 num_rep_block=(4, 4)):
        self.num_classes = num_classes
        self.max_len = max_len
        self.cnn_filter_size = cnn_filter_size
        self.pooling_filter_size = pooling_filter_size
        self.num_filters_per_size = num_filters_per_size
        self.num_rep_block = num_rep_block

    def __call__(self, inputs):

        inputs = tf.reshape(inputs, [-1, 4, self.max_len, 1])

        inputs = slim.conv2d(inputs=inputs,
                             num_outputs=self.num_filters_per_size[0],
                             kernel_size=[4, self.cnn_filter_size[0]],
                             weights_initializer=tf.contrib.layers.variance_scaling_initializer(
                                 factor=1.0, mode='FAN_AVG', uniform=True),
                             normalizer_fn=slim.batch_norm, scope='conv0', padding='SAME')

        for i in range(0, len(self.num_filters_per_size)):
            inputs = dense_block(inputs,
                                 self.num_filters_per_size[i],
                                 self.cnn_filter_size[i],
                                 self.num_rep_block[i])

            # Transition Layer
            if i != len(self.num_filters_per_size) - 1:
                inputs = slim.conv2d(inputs,
                                     self.num_filters_per_size[i + 1],
                                     [1, self.cnn_filter_size[i]],
                                     weights_initializer=tf.contrib.layers.variance_scaling_initializer(
                                         factor=1.0, mode='FAN_AVG', uniform=True),
                                     normalizer_fn=slim.batch_norm,
                                     scope='conv-last-%s' % i)

                # Max pooling 1/2
                inputs = slim.max_pool2d(inputs,
                                         [1, self.pooling_filter_size[i]],
                                         stride=self.pooling_filter_size[i],
                                         scope='pool_%s' % i)

        inputs = tf.nn.top_k(tf.transpose(inputs, [0, 1, 3, 2]), k=8, name='k_max_pool', sorted=False)[0]

        inputs = slim.flatten(inputs)
        inputs = slim.fully_connected(inputs, 2048, scope='FC1')
        inputs = slim.fully_connected(inputs, 2048, scope='FC2')
        logits = slim.fully_connected(inputs, self.num_classes, activation_fn=None, scope='output')

        return logits


