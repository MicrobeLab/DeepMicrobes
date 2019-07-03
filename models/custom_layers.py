from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import tensorflow.contrib.slim as slim


def embedding_layer(inputs, vocab_size, embedding_dim, initializer):
    """Looks up embedding vectors for each k-mer."""
    embedding_weights = tf.get_variable(name="token_embedding_weights",
                                        shape=[vocab_size, embedding_dim],
                                        initializer=initializer, trainable=True)
    return tf.nn.embedding_lookup(embedding_weights, inputs)


def bidirectional_lstm(inputs, lstm_dim, length_list, batch_size, initializer):
    """Computes the hidden state of bidirectional lstm."""
    # Modified from implementation by Diego Antognini available at:
    # https://github.com/Diego999/SelfSent
    lstm_cell = {}
    initial_state = {}

    for direction in ["forward", "backward"]:
        with tf.variable_scope(direction):
            lstm_cell[direction] = tf.contrib.rnn.CoupledInputForgetGateLSTMCell(
                lstm_dim, forget_bias=1.0, initializer=initializer,
                state_is_tuple=True)
            initial_cell_state = tf.get_variable("initial_cell_state",
                                                 shape=[1, lstm_dim],
                                                 dtype=tf.float32,
                                                 initializer=initializer)
            initial_output_state = tf.get_variable("initial_output_state",
                                                   shape=[1, lstm_dim],
                                                   dtype=tf.float32,
                                                   initializer=initializer)
            c_states = tf.tile(initial_cell_state, tf.stack([batch_size, 1]))
            h_states = tf.tile(initial_output_state, tf.stack([batch_size, 1]))
            initial_state[direction] = tf.contrib.rnn.LSTMStateTuple(c_states, h_states)

    (outputs_forward, outputs_backward), final_states = tf.nn.bidirectional_dynamic_rnn(
        lstm_cell["forward"], lstm_cell["backward"], inputs,
        sequence_length=length_list, dtype=tf.float32,
        initial_state_fw=initial_state["forward"], initial_state_bw=initial_state["backward"])

    inputs = tf.concat([outputs_forward, outputs_backward], axis=2)

    return inputs


def batch_stat(inputs):
    """Computes tokenized reads length in a batch and batch size.

    Returns:
        length_list: a tensor of tokenized reads length in shape [batch_size].
        length_max: the maximum length in a batch.
        batch_size: dynamically computed batch size.
    """
    used = tf.sign(tf.reduce_max(tf.abs(inputs), 2))
    length = tf.reduce_sum(used, 1)
    length_list = tf.cast(length, tf.int32)
    length_max = tf.reduce_max(length_list)
    batch_size = tf.shape(inputs)[0]
    return length_list, length_max, batch_size


def dense_block(input_layer, num_filters_per_size_i, cnn_filter_size_i, num_rep_block_i):
    # Modified from implementation by Hoa T. Le available at:
    # https://github.com/lethienhoa/Very-Deep-Convolutional-Networks-for-Natural-Language-Processing
    nodes = []
    a = slim.conv2d(input_layer, num_filters_per_size_i, [1, cnn_filter_size_i],
                    weights_initializer=tf.contrib.layers.variance_scaling_initializer(
                        factor=1.0, mode='FAN_AVG', uniform=True),
                    normalizer_fn=slim.batch_norm)
    nodes.append(a)
    for z in range(num_rep_block_i-1):
        b = slim.conv2d(tf.concat(nodes, 3), num_filters_per_size_i, [1, cnn_filter_size_i],
                        weights_initializer=tf.contrib.layers.variance_scaling_initializer(
                            factor=1.0, mode='FAN_AVG', uniform=True),
                        normalizer_fn=slim.batch_norm)
        nodes.append(b)
    return b


def attention_layer(inputs, lstm_dim, da, row, length_max, initializer):
    """Creates the attention layer and applies it to the LSTM hidden state
    to generate the embedding matrix.
    """
    ws1 = tf.get_variable("ws1", shape=[2 * lstm_dim, da],
                          initializer=initializer, trainable=True)
    intermediate_inputs_1 = tf.reshape(inputs, [-1, 2 * lstm_dim])
    intermediate_inputs_1 = tf.nn.tanh(tf.matmul(intermediate_inputs_1, ws1))
    ws2 = tf.get_variable("ws2", shape=[da, row], initializer=initializer)
    intermediate_inputs_1 = tf.matmul(intermediate_inputs_1, ws2)
    intermediate_inputs_1 = tf.nn.softmax(tf.reshape(
        intermediate_inputs_1, shape=[-1, length_max, row]), dim=1)

    intermediate_inputs_2 = tf.transpose(inputs, perm=[0, 2, 1])
    inputs = tf.matmul(intermediate_inputs_2, intermediate_inputs_1)

    return inputs

