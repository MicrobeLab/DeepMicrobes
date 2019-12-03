from Bio import SeqIO
import numpy as np
import tensorflow as tf
import argparse
import sys


def wrap_int64(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def wrap_float(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value.reshape(-1)))


def base2vector(base):
    ambiguity_dict = {'A': [1, 0, 0, 0], 'C': [0, 1, 0, 0], 'G': [0, 0, 1, 0], 'T': [0, 0, 0, 1],
                      'K': [0, 0, 0.5, 0.5], 'M': [0.5, 0.5, 0, 0], 'R': [0.5, 0, 0.5, 0],
                      'Y': [0, 0.5, 0, 0.5], 'S': [0, 0.5, 0.5, 0], 'W': [0.5, 0, 0, 0.5],
                      'B': [0, 0.33, 0.33, 0.33], 'V': [0.33, 0.33, 0.33, 0], 'H': [0.33, 0.33, 0, 0.33],
                      'D': [0.33, 0, 0.33, 0.33], 'X': [0.25, 0.25, 0.25, 0.25], 'N': [0.25, 0.25, 0.25, 0.25]}
    vector = ambiguity_dict[base]
    return vector


def seq2array(seq):
    bp = len(seq)
    array = np.zeros((bp, 4))
    for i, base in enumerate(seq):
        array[i, :] = base2vector(base)
    return array


def train_parse(rec):
    seq = rec.seq
    array = seq2array(seq)
    identifier = rec.id
    label = int(identifier.split('|')[1])
    return array, label


def predict_parse(rec):
    seq = rec.seq
    array = seq2array(seq)
    return array


def convert_advance_file(input_file, output_tfrecord, seq_type):
    with tf.python_io.TFRecordWriter(output_tfrecord) as writer:
        with open(input_file) as handle:
            for rec in SeqIO.parse(handle, seq_type):
                array, label = train_parse(rec)
                data = \
                    {
                        'read': wrap_float(array),
                        'label': wrap_int64(label)
                    }
                feature = tf.train.Features(feature=data)
                example = tf.train.Example(features=feature)
                serialized = example.SerializeToString()
                writer.write(serialized)
    return


def convert_advance_file_predict(input_file, output_tfrecord, seq_type):
    with tf.python_io.TFRecordWriter(output_tfrecord) as writer:
        with open(input_file) as handle:
            for rec in SeqIO.parse(handle, seq_type):
                array = predict_parse(rec)
                data = \
                    {
                        'read': wrap_float(array)
                    }
                feature = tf.train.Features(feature=data)
                example = tf.train.Example(features=feature)
                serialized = example.SerializeToString()
                writer.write(serialized)
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_seq')
    parser.add_argument('--output_tfrec')
    parser.add_argument('--is_train', default=False, help='mode')
    parser.add_argument('--seq_type', default='fasta', help='fasta/fastq')
    args = parser.parse_args()
    input_fasta = args.input_seq
    output_tfrecord = args.output_tfrec
    is_train = args.is_train
    seq_type = args.seq_type
    if is_train:
        convert_advance_file(input_fasta, output_tfrecord, seq_type)
    else:
        convert_advance_file_predict(input_fasta, output_tfrecord, seq_type)
    return


if __name__ == '__main__':
    main()


