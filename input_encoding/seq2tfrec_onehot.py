from Bio import SeqIO
import numpy as np
import tensorflow as tf
import argparse
import sys


def wrap_int64(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def wrap_float(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value.reshape(-1)))


def label_dict(label_file):
    lab_dic = {}
    with open(label_file) as handle:
        for line in handle:
            line_ls = line.rstrip().split('\t')
            label_id = int(line_ls[0])
            taxon_id = int(line_ls[1])
            lab_dic[taxon_id] = label_id
    return lab_dic


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


def metasim_parse(rec):
    seq = rec.seq
    array = seq2array(seq)
    description = rec.description
    taxon_id = description.split('|')[4]
    taxon_id = int(taxon_id)
    return array, taxon_id


def art_parse(rec):
    seq = rec.seq
    array = seq2array(seq)
    identifier = rec.id
    taxon_id = identifier.split('|')[1]
    taxon_id = int(taxon_id)
    return array, taxon_id

def predict_parse(rec):
    seq = rec.seq
    array = seq2array(seq)
    return array

def convert_advance_file(input_file, output_tfrecord, label_file, software):
    lab_dic = label_dict(label_file)
    with tf.python_io.TFRecordWriter(output_tfrecord) as writer:
        with open(input_file) as handle:
            for rec in SeqIO.parse(handle, 'fasta'):
                if software == 'art':
                    array, taxon_id = art_parse(rec)
                if software == 'metasim':
                    array, taxon_id = metasim_parse(rec)
                label = lab_dic[taxon_id]
                data = \
                    {
                        'read': wrap_float(array),
                        'label': wrap_int64(label)
                    }
                feature = tf.train.Features(feature=data)
                example = tf.train.Example(features=feature)
                serialized = example.SerializeToString()
                writer.write(serialized)


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


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_seq')
    parser.add_argument('--output_tfrec')
    parser.add_argument('--label', default='lable2taxid.txt')
    parser.add_argument('--software', default='art', help='art/metasim')
    parser.add_argument('--is_train', default=False, help='mode')
    parser.add_argument('--seq_type', default='fasta', help='fasta/fastq')
    args = parser.parse_args()
    input_fasta = args.input_seq
    output_tfrecord = args.output_tfrec
    label_file = args.label_file
    software = args.software
    is_train = args.is_train
    seq_type = args.seq_type
    if is_train:
        convert_advance_file(input_fasta, output_tfrecord, label_file, software)
    else:
        convert_advance_file_predict(input_fasta, output_tfrecord, seq_type)
    return


if __name__ == '__main__':
    main(sys.argv)

