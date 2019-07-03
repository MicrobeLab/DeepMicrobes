"""Modified codes from 
https://github.com/tensorflow/models/tree/master/research/seq2species
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import math


spatial_conv_width = [5, 9, 13]
pointwise_conv_depth = [84, 58, 180]
fc_unit = 2828
leaky_relu_slope = 1.2538e-2
learning_rate = 4.6969e-4
decay_rate = 6.5505e-2
keep_prob = 0.94018
weight_init_scale = 1.1841


def init_weights(shape, scale=1.0, name='weights'):
    """Randomly initializes a weight Tensor of the given shape.

    Args:
      shape: list; desired Tensor dimensions.
      scale: float; standard deviation scale with which to initialize weights.
      name: string name for the variable.

    Returns:
      TF Variable contining truncated random Normal initialized weights.
    """
    num_inputs = shape[0] if len(shape) < 3 else shape[0] * shape[1] * shape[2]
    stddev = scale / math.sqrt(num_inputs)
    return tf.get_variable(
        name,
        shape=shape,
        initializer=tf.truncated_normal_initializer(0., stddev))


def init_bias(size):
    """Initializes bias vector of given shape as zeros.

    Args:
      size: int; desired size of bias Tensor.

    Returns:
      TF Variable containing the initialized biases.
    """
    return tf.get_variable(
        name='b_{}'.format(size),
        shape=[size],
        initializer=tf.zeros_initializer())


def summary_scalar(name, scalar):
    """Adds a summary scalar, if the platform supports summaries."""
    return tf.summary.scalar(name, scalar)


def summary_histogram(name, values):
    """Adds a summary histogram, if the platform supports summaries."""
    return tf.summary.histogram(name, values)


def convolution(inputs, filter_dim, pointwise_dim=None, scale=1.0, padding='SAME'):
    """Applies convolutional filter of given dimensions to given input Tensor.

    If a pointwise dimension is specified, a depthwise separable convolution is
    performed.

    Args:
      inputs: 4D Tensor of shape (# reads, 1, # basepairs, # bases).
      filter_dim: integer tuple of the form (width, depth).
      pointwise_dim: int; output dimension for pointwise convolution.
      scale: float; standard deviation scale with which to initialize weights.
      padding: string; type of padding to use. One of "SAME" or "VALID".

    Returns:
      4D Tensor result of applying the convolutional filter to the inputs.
    """
    in_channels = inputs.get_shape()[3].value
    filter_width, filter_depth = filter_dim
    filters = init_weights([1, filter_width, in_channels, filter_depth], scale, name='weights')
    #summary_histogram(filters.name.split(':')[0].split('/')[1], filters)
    if pointwise_dim is None:
        return tf.nn.conv2d(
            inputs,
            filters,
            strides=[1, 1, 1, 1],
            padding=padding,
            name='weights')
    pointwise_filters = init_weights([1, 1, filter_depth * in_channels, pointwise_dim], scale, name='pointwise_weights')
    #summary_histogram(pointwise_filters.name.split(':')[0].split('/')[1], pointwise_filters)
    return tf.nn.separable_conv2d(
        inputs,
        filters,
        pointwise_filters,
        strides=[1, 1, 1, 1],
        padding=padding)


def pool(inputs):
    """Performs pooling across width and height of the given inputs.

    Args:
      inputs: Tensor shaped (batch, height, width, channels) over which to pool.
        In our case, height is a unitary dimension and width can be thought of
        as the read dimension.
      pooling_type: string; one of "avg" or "max".

    Returns:
      Tensor result of performing pooling of the given pooling_type over the
      height and width dimensions of the given inputs.
    """
    return tf.reduce_sum(inputs, axis=[1, 2]) / tf.to_float(tf.shape(inputs)[2])


def leaky_relu(lrelu_slope, inputs):
    """Applies leaky ReLu activation to the given inputs with the given slope.

    Args:
      lrelu_slope: float; slope value for the activation function.
        A slope of 0.0 defines a standard ReLu activation, while a positive
        slope defines a leaky ReLu.
      inputs: Tensor upon which to apply the activation function.

    Returns:
      Tensor result of applying the activation function to the given inputs.
    """
    return tf.maximum(lrelu_slope * inputs, inputs)


def dropout(inputs, keep_prob):
    """Applies dropout to the given inputs.

    Args:
      inputs: Tensor upon which to apply dropout.
      keep_prob: float; probability with which to randomly retain values in
        the given input.

    Returns:
      Tensor result of applying dropout to the given inputs.
    """
    return tf.nn.dropout(inputs, keep_prob)


class Seq2species(object):
    def __init__(self, num_classes, max_len=100, is_train=False):
        self.num_classes = num_classes
        self.max_len = max_len
        self.is_train = is_train

    def __call__(self, inputs):
        # inputs = tf.reshape(inputs, [-1, self.max_len, 4])
        x = tf.reshape(inputs, [-1, 1, self.max_len, 4], name='reshape_input')

        # first depth-wise separable conv
        with tf.variable_scope('convolution_1'):
            x = convolution(x, (spatial_conv_width[0], 1), pointwise_conv_depth[0], weight_init_scale)
            x = leaky_relu(leaky_relu_slope, x)
            if self.is_train:
                x = dropout(x, keep_prob)

        # second depth-wise separable conv
        with tf.variable_scope('convolution_2'):
            x = convolution(x, (spatial_conv_width[1], 1), pointwise_conv_depth[1], weight_init_scale)
            x = leaky_relu(leaky_relu_slope, x)
            if self.is_train:
                x = dropout(x, keep_prob)

        # third depth-wise separable conv
        with tf.variable_scope('convolution_3'):
            x = convolution(x, (spatial_conv_width[2], 1), pointwise_conv_depth[2], weight_init_scale)
            x = leaky_relu(leaky_relu_slope, x)
            if self.is_train:
                x = dropout(x, keep_prob)

        # first fc
        with tf.variable_scope('fc_1'):
            biases = init_bias(fc_unit)
            filter_dimensions = (self.max_len, fc_unit)
            x = biases + convolution(x, filter_dimensions, scale=weight_init_scale, padding='VALID')
            # summary_histogram(biases.name.split(':')[0].split('/')[1], biases)
            x = leaky_relu(leaky_relu_slope, x)
            if self.is_train:
                x = dropout(x, keep_prob)

        # second fc
        with tf.variable_scope('fc_2'):
            biases = init_bias(fc_unit)
            filter_dimensions = (1, fc_unit)
            x = biases + convolution(x, filter_dimensions, scale=weight_init_scale, padding='VALID')
            # summary_histogram(biases.name.split(':')[0].split('/')[1], biases)
            x = leaky_relu(leaky_relu_slope, x)
            if self.is_train:
                x = dropout(x, keep_prob)

        # pooling
        with tf.variable_scope('avg_pooling'):
            x = pool(x)

        # output layer
        with tf.variable_scope('output_layer'):
            weights = init_weights([x.get_shape()[1].value, self.num_classes], scale=weight_init_scale, name='weights')
            biases = init_bias(self.num_classes)
            logits = tf.matmul(x, weights) + biases

        return logits
