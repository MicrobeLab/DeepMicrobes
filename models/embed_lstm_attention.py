from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import tensorflow as tf
from models.custom_layers import batch_stat_for_kmer_encoding, embedding_layer, bidirectional_lstm, attention_layer


class EmbedAttention(object):
    def __init__(self, num_classes, lstm_dim, mlp_dim,
                 vocab_size, embedding_dim, row, da, keep_prob):
        self.num_classes = num_classes
        self.lstm_dim = lstm_dim
        self.mlp_dim = mlp_dim
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.row = row
        self.da = da
        self.keep_prob = keep_prob

    def __call__(self, inputs):
        initializer = tf.contrib.layers.xavier_initializer()
	
        length_list, length_max, batch_size = batch_stat_for_kmer_encoding(inputs)

        with tf.variable_scope("token_embedding"):
            inputs = embedding_layer(inputs, self.vocab_size,
                                     self.embedding_dim, initializer)

        #length_list, length_max, batch_size = batch_stat(inputs)

        with tf.variable_scope("token_lstm"):
            inputs = bidirectional_lstm(inputs, self.lstm_dim, length_list,
                                        batch_size, initializer)

        with tf.variable_scope("attention"):
            inputs = attention_layer(inputs, self.lstm_dim, self.da,
                                     self.row, length_max, initializer)

        with tf.variable_scope("layer_ReLU_1"):
            inputs = tf.reshape(inputs, shape=[-1, self.row * 2 * self.lstm_dim])
            w_relu_1 = tf.get_variable("w_relu_1",
                                       shape=[self.row * 2 * self.lstm_dim, self.mlp_dim],
                                       initializer=initializer)
            b_relu_1 = tf.Variable(tf.constant(0.0, shape=[self.mlp_dim]))
            inputs = tf.nn.relu(tf.nn.xw_plus_b(inputs, w_relu_1, b_relu_1))
            inputs = tf.nn.dropout(inputs, self.keep_prob)

        with tf.variable_scope("layer_ReLU_2"):
            w_relu_2 = tf.get_variable("w_relu_2", shape=[self.mlp_dim, self.mlp_dim],
                                       initializer=initializer)
            b_relu_2 = tf.Variable(tf.constant(0.0, shape=[self.mlp_dim]))
            inputs = tf.nn.relu(tf.nn.xw_plus_b(inputs, w_relu_2, b_relu_2))
            inputs = tf.nn.dropout(inputs, self.keep_prob)

        with tf.variable_scope("layer_output"):
            w_output = tf.get_variable("w_output",
                                       shape=[self.mlp_dim, self.num_classes],
                                       initializer=initializer)
            b_output = tf.Variable(tf.constant(0.0, shape=[self.num_classes]))
            logits = tf.nn.xw_plus_b(inputs, w_output, b_output)

        return logits
