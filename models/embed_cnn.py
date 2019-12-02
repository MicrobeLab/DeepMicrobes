from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from models.custom_layers import embedding_layer


class EmbedCNN(object):
    def __init__(self, num_classes, vocab_size, embedding_dim, mlp_dim,
                 cnn_filter_sizes, cnn_num_filters,
                 kmer=12, max_len=100):
        self.num_classes = num_classes
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.mlp_dim = mlp_dim
        self.cnn_filter_sizes = cnn_filter_sizes
        self.cnn_num_filters = cnn_num_filters
        self.input_len = max_len - kmer + 1

    def __call__(self, inputs):
        initializer = tf.contrib.layers.xavier_initializer()
        inputs = embedding_layer(inputs, self.vocab_size, self.embedding_dim,
                                 initializer)
        inputs = tf.expand_dims(inputs, axis=-1)

        # Create a convolution + max-pool layer for each filter size
        pooled_outputs = []
        for i, filter_size in enumerate(self.cnn_filter_sizes):
            with tf.name_scope("conv-maxpool-%s" % filter_size):
                # Convolution Layer
                filter_shape = [filter_size, self.embedding_dim, 1, self.cnn_num_filters]
                W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
                b = tf.Variable(tf.constant(0.1, shape=[self.cnn_num_filters]), name="b")
                conv = tf.nn.conv2d(
                    inputs,
                    W,
                    strides=[1, 1, 1, 1],
                    padding="VALID",
                    name="conv")
                # Apply non-linearity
                h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")
                # Maxpooling over the outputs
                pooled = tf.nn.max_pool(
                    h,
                    ksize=[1, self.input_len - filter_size + 1, 1, 1],
                    strides=[1, 1, 1, 1],
                    padding='VALID',
                    name="pool")
                pooled_outputs.append(pooled)

        # Combine all the pooled features
        num_filters_total = self.cnn_num_filters * len(self.cnn_filter_sizes)
        inputs = tf.concat(pooled_outputs, 3)
        inputs = tf.reshape(inputs, [-1, num_filters_total])

        with tf.variable_scope("layer_ReLU_1"):
            w_relu_1 = tf.get_variable("w_relu_1",
                                       shape=[num_filters_total, self.mlp_dim],
                                       initializer=initializer)
            b_relu_1 = tf.Variable(tf.constant(0.0, shape=[self.mlp_dim]))
            inputs = tf.nn.relu(tf.nn.xw_plus_b(inputs, w_relu_1, b_relu_1))

        with tf.variable_scope("layer_ReLU_2"):
            w_relu_2 = tf.get_variable("w_relu_2", shape=[self.mlp_dim, self.mlp_dim],
                                       initializer=initializer)
            b_relu_2 = tf.Variable(tf.constant(0.0, shape=[self.mlp_dim]))
            inputs = tf.nn.relu(tf.nn.xw_plus_b(inputs, w_relu_2, b_relu_2))

        with tf.variable_scope("layer_output"):
            w_output = tf.get_variable("w_output",
                                       shape=[self.mlp_dim, self.num_classes],
                                       initializer=initializer)
            b_output = tf.Variable(tf.constant(0.0, shape=[self.num_classes]))
            logits = tf.nn.xw_plus_b(inputs, w_output, b_output)

        return logits


class EmbedCNNnoPool(object):
    def __init__(self, num_classes, vocab_size, embedding_dim, mlp_dim,
                 cnn_filter_sizes, cnn_num_filters,
                 kmer=12, max_len=100):
        self.num_classes = num_classes
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.mlp_dim = mlp_dim
        self.cnn_filter_sizes = cnn_filter_sizes
        self.cnn_num_filters = cnn_num_filters
        self.input_len = max_len - kmer + 1

    def __call__(self, inputs):
        initializer = tf.contrib.layers.xavier_initializer()
        inputs = embedding_layer(inputs, self.vocab_size, self.embedding_dim,
                                 initializer)
        inputs = tf.expand_dims(inputs, axis=-1)

        cnn_feature_maps = []
        for i, filter_size in enumerate(self.cnn_filter_sizes):
            with tf.name_scope("conv-filter-size-%s" % filter_size):
                # Convolution Layer
                filter_shape = [filter_size, self.embedding_dim, 1, self.cnn_num_filters]
                W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
                b = tf.Variable(tf.constant(0.1, shape=[self.cnn_num_filters]), name="b")
                conv = tf.nn.conv2d(
                    inputs,
                    W,
                    strides=[1, 1, 1, 1],
                    padding="SAME",
                    data_format='NHWC',
                    name="conv")
                # Apply non-linearity
                activated_cnn = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")
                cnn_feature_maps.append(activated_cnn)

        inputs = tf.concat(cnn_feature_maps, 3)
        inputs = tf.layers.flatten(inputs)

        cnn_feature_dim = (self.input_len-self.cnn_filter_sizes[0]) * self.cnn_num_filters * len(self.cnn_filter_sizes)
        #cnn_feature_dimension = 0
        #for filter_size in self.cnn_filter_sizes:
            #cnn_feature_dimension += (self.input_len - filter_size + 1) * self.cnn_num_filters

        with tf.variable_scope("layer_ReLU_1"):
            w_relu_1 = tf.get_variable("w_relu_1",
                                       shape=[cnn_feature_dim, self.mlp_dim],
                                       initializer=initializer)
            b_relu_1 = tf.Variable(tf.constant(0.0, shape=[self.mlp_dim]))
            inputs = tf.nn.relu(tf.nn.xw_plus_b(inputs, w_relu_1, b_relu_1))

        with tf.variable_scope("layer_ReLU_2"):
            w_relu_2 = tf.get_variable("w_relu_2", shape=[self.mlp_dim, self.mlp_dim],
                                       initializer=initializer)
            b_relu_2 = tf.Variable(tf.constant(0.0, shape=[self.mlp_dim]))
            inputs = tf.nn.relu(tf.nn.xw_plus_b(inputs, w_relu_2, b_relu_2))

        with tf.variable_scope("layer_output"):
            w_output = tf.get_variable("w_output",
                                       shape=[self.mlp_dim, self.num_classes],
                                       initializer=initializer)
            b_output = tf.Variable(tf.constant(0.0, shape=[self.num_classes]))
            logits = tf.nn.xw_plus_b(inputs, w_output, b_output)

        return logits




