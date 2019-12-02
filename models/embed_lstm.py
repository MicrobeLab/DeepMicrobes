from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import tensorflow as tf
from models.custom_layers import batch_stat_for_kmer_encoding, \
    embedding_layer, bidirectional_lstm


class EmbedLSTM(object):
    def __init__(self, num_classes, lstm_dim, mlp_dim,
                 vocab_size, embedding_dim, kmer, max_len,
                 pooling_type='none'):
        self.num_classes = num_classes
        self.lstm_dim = lstm_dim
        self.mlp_dim = mlp_dim
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.pooling_type = pooling_type
        self.kernel_size = max_len - kmer + 1

    def __call__(self, inputs):
        initializer = tf.contrib.layers.xavier_initializer()

        length_list, length_max, batch_size = batch_stat_for_kmer_encoding(inputs)

        with tf.variable_scope("token_embedding"):
            inputs = embedding_layer(inputs, self.vocab_size,
                                     self.embedding_dim, initializer)

        with tf.variable_scope("token_lstm"):
            inputs = bidirectional_lstm(inputs, self.lstm_dim, length_list,
                                        batch_size, initializer)

        with tf.variable_scope("pooling"):
            inputs = tf.expand_dims(inputs, axis=-1)
            if self.pooling_type == 'avg':
                inputs = tf.nn.avg_pool(inputs, [1, self.kernel_size, 1, 1], [1, 1, 1, 1], 'VALID')
                inputs = tf.reshape(inputs, shape=[-1, 2 * self.lstm_dim])
                w_relu_1 = tf.get_variable("w_relu_1",
                                           shape=[2 * self.lstm_dim, self.mlp_dim],
                                           initializer=initializer)
            elif self.pooling_type == 'max':
                inputs = tf.nn.max_pool(inputs, [1, self.kernel_size, 1, 1], [1, 1, 1, 1], 'VALID')
                inputs = tf.reshape(inputs, shape=[-1, 2 * self.lstm_dim])
                w_relu_1 = tf.get_variable("w_relu_1",
                                           shape=[2 * self.lstm_dim, self.mlp_dim],
                                           initializer=initializer)
            elif self.pooling_type == 'concat':
                avg_pool = tf.nn.avg_pool(inputs, [1, self.kernel_size, 1, 1], [1, 1, 1, 1], 'VALID')
                max_pool = tf.nn.max_pool(inputs, [1, self.kernel_size, 1, 1], [1, 1, 1, 1], 'VALID')
                inputs = tf.concat([avg_pool, max_pool], 1)
                inputs = tf.reshape(inputs, shape=[-1, 2 * 2 * self.lstm_dim])
                w_relu_1 = tf.get_variable("w_relu_1",
                                           shape=[2 * 2 * self.lstm_dim, self.mlp_dim],
                                           initializer=initializer)
            else:
                inputs = tf.reshape(inputs, shape=[-1, 2 * self.lstm_dim * self.kernel_size])
                w_relu_1 = tf.get_variable("w_relu_1",
                                           shape=[2 * self.lstm_dim * self.kernel_size, self.mlp_dim],
                                           initializer=initializer)

        with tf.variable_scope("layer_ReLU_1"):
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


