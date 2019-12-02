from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from models.custom_layers import embedding_layer


class EmbedPool(object):
    def __init__(self, num_classes, vocab_size, embedding_dim, mlp_dim,
                 kmer=12, max_len=100):
        self.num_classes = num_classes
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.mlp_dim = mlp_dim
        self.kernel_size = max_len - kmer + 1

    def __call__(self, inputs):
        initializer = tf.contrib.layers.xavier_initializer()
        inputs = embedding_layer(inputs, self.vocab_size, self.embedding_dim,
                                 initializer)
        inputs = tf.expand_dims(inputs, axis=-1)
        avg_pool = tf.nn.avg_pool(inputs, [1, self.kernel_size, 1, 1], [1, 1, 1, 1], 'VALID')
        max_pool = tf.nn.max_pool(inputs, [1, self.kernel_size, 1, 1], [1, 1, 1, 1], 'VALID')
        inputs = tf.concat([avg_pool, max_pool], 1)
        inputs = tf.squeeze(inputs)
        #bias_init = tf.constant_initializer(0.001, dtype=tf.float32)

        with tf.variable_scope("layer_ReLU_1"):
            inputs = tf.reshape(inputs, shape=[-1, self.embedding_dim * 2])
            w_relu_1 = tf.get_variable("w_relu_1",
                                       shape=[self.embedding_dim * 2, self.mlp_dim],
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
        #inputs = layers.fully_connected(inputs, num_outputs=self.mlp_dim,
                                        #activation_fn=tf.nn.relu,
                                        #biases_initializer=bias_init,
                                        #scope='mlp_1', reuse=None)
        #inputs = layers.fully_connected(inputs, num_outputs=self.mlp_dim,
                                        #activation_fn=tf.nn.relu,
                                        #biases_initializer=bias_init,
                                        #scope='mlp_2', reuse=None)
        #logits = layers.linear(inputs, num_outputs=self.num_classes,
                               #biases_initializer=bias_init,
                               #scope='output_logits', reuse=None)

        return logits






