from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf


def input_function_train_kmer(input_tfrec, repeat_count, batch_size, cpus):
    """Parses tfrecord and returns dataset for training/eval.

    Args:
        input_tfrec: Filenames of tfrecord.
        repeat_count: Number of epochs.
        batch_size: Number of examples returned per iteration.
        cpus: Number of cores used to running input pipeline.

    Returns:
        Dataset of (reads, label) pairs.
    """

    def _parse_function(serialized):
        features = \
            {
                'read': tf.FixedLenSequenceFeature([], tf.int64, allow_missing=True),
                'label': tf.FixedLenSequenceFeature([], tf.int64, allow_missing=True)
            }
        parsed_example = tf.parse_single_example(
            serialized=serialized, features=features)
        read = parsed_example['read']
        label = parsed_example['label']
        d = read, label
        return d

    files = tf.data.Dataset.list_files(input_tfrec)
    dataset = files.apply(tf.contrib.data.parallel_interleave(
        tf.data.TFRecordDataset, cycle_length=cpus))
    dataset = dataset.apply(tf.contrib.data.shuffle_and_repeat(
        buffer_size=batch_size * 5, count=repeat_count))
    dataset = dataset.apply(
        tf.contrib.data.map_and_batch(map_func=_parse_function,
                                      batch_size=batch_size,
                                      num_parallel_calls=cpus))
    dataset = dataset.prefetch(buffer_size=None)
    iterator = dataset.make_one_shot_iterator()
    batch_features, batch_labels = iterator.get_next()
    return batch_features, batch_labels


def input_function_predict_kmer(input_tfrec, batch_size, cpus):
    """Parses tfrecord and returns dataset for prediction.

    Args:
        input_tfrec: Filenames of tfrecord.
        batch_size: Number of examples returned per iteration.
        cpus: Number of cores used to running input pipeline.

    Returns:
        Dataset of reads ready for species prediction.
    """

    def _parse_function(serialized):
        features = \
            {
                'read': tf.FixedLenSequenceFeature([], tf.int64, allow_missing=True)
            }
        parsed_example = tf.parse_single_example(
            serialized=serialized, features=features)
        read = parsed_example['read']
        d = read
        return d

    files = tf.data.Dataset.list_files(input_tfrec)
    dataset = files.apply(tf.contrib.data.parallel_interleave(
        tf.data.TFRecordDataset, cycle_length=cpus))
    dataset = dataset.apply(
        tf.contrib.data.map_and_batch(map_func=_parse_function,
                                      batch_size=batch_size,
                                      num_parallel_calls=cpus))
    dataset = dataset.prefetch(buffer_size=None)
    iterator = dataset.make_one_shot_iterator()
    batch_features = iterator.get_next()
    return batch_features


def input_function_train_one_hot(input_tfrec, repeat_count, batch_size, cpus):
    """Parses tfrecord and returns dataset for training/eval.

    Args:
        input_tfrec: Filenames of tfrecord.
        repeat_count: Number of epochs.
        batch_size: Number of examples returned per iteration.
        cpus: Number of cores used to running input pipeline.

    Returns:
        Dataset of (reads, label) pairs.
    """

    def _parse_function(serialized):
        features = \
            {
                'read': tf.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
                'label': tf.FixedLenSequenceFeature([], tf.int64, allow_missing=True)
            }
        parsed_example = tf.parse_single_example(
            serialized=serialized, features=features)
        read = parsed_example['read']
        label = parsed_example['label']
        d = read, label
        return d

    files = tf.data.Dataset.list_files(input_tfrec)
    dataset = files.apply(tf.contrib.data.parallel_interleave(
        tf.data.TFRecordDataset, cycle_length=cpus))
    dataset = dataset.apply(tf.contrib.data.shuffle_and_repeat(
        buffer_size=batch_size * 5, count=repeat_count))
    dataset = dataset.apply(
        tf.contrib.data.map_and_batch(map_func=_parse_function,
                                      batch_size=batch_size,
                                      num_parallel_calls=cpus))
    dataset = dataset.prefetch(buffer_size=None)
    iterator = dataset.make_one_shot_iterator()
    batch_features, batch_labels = iterator.get_next()
    return batch_features, batch_labels


def input_function_predict_one_hot(input_tfrec, batch_size, cpus):
    """Parses tfrecord and returns dataset for prediction.

    Args:
        input_tfrec: Filenames of tfrecord.
        batch_size: Number of examples returned per iteration.
        cpus: Number of cores used to running input pipeline.

    Returns:
        Dataset of reads ready for species prediction.
    """

    def _parse_function(serialized):
        features = \
            {
                'read': tf.FixedLenSequenceFeature([], tf.float32, allow_missing=True)
            }
        parsed_example = tf.parse_single_example(
            serialized=serialized, features=features)
        read = parsed_example['read']
        d = read
        return d

    files = tf.data.Dataset.list_files(input_tfrec)
    dataset = files.apply(tf.contrib.data.parallel_interleave(
        tf.data.TFRecordDataset, cycle_length=cpus))
    dataset = dataset.apply(
        tf.contrib.data.map_and_batch(map_func=_parse_function,
                                      batch_size=batch_size,
                                      num_parallel_calls=cpus))
    dataset = dataset.prefetch(buffer_size=None)
    iterator = dataset.make_one_shot_iterator()
    batch_features = iterator.get_next()
    return batch_features
