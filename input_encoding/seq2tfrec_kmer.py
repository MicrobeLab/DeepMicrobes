"""Converts DNA sequences to tfrecord.

Input sequences should be in fasta or fastq format.

The script depends on a vocabulary file containing all possible k-mers plus an 
<unk> sign, one per line. (E.g. The vocabulary size is 8390657 when k = 12.)

If is_train is True, the script additionally requires a tab-delimited label file 
mapping from label to species taxid.

You can run the script using the following command.
```
python seq2tfrec_kmer.py \
  --input_seq example.fasta \
  --output_tfrec example.tfrec \
  --kmer 12 \
  --vocab vocabulary_12mers.txt \
  --label label2taxid.txt \
  --is_train True \
  --seq_type fasta
```

Reads will be split into (length - kmer + 1) k-mers as tokens.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import numpy as np
from Bio import SeqIO
from absl import app as absl_app
from absl import flags
import tensorflow as tf

from utils.flags import core as flags_core


def forward2reverse(dna):
    """Converts an oligonucleotide(k-mer) to its reverse complement sequence.
    All ambiguous bases are treated as Ns.
    """
    translation_dict = {"A": "T", "T": "A", "C": "G", "G": "C", "N": "N",
                        "K": "N", "M": "N", "R": "N", "Y": "N", "S": "N",
                        "W": "N", "B": "N", "V": "N", "H": "N", "D": "N",
                        "X": "N"}
    letters = list(dna)
    letters = [translation_dict[base] for base in letters]
    return ''.join(letters)[::-1]


def label_dict(label_file):
    """Turns the label info into a dict={label: taxid}."""
    lab_dic = {}
    with open(label_file) as handle:
        for line in handle:
            line_ls = line.rstrip().split('\t')
            label_id = int(line_ls[0])
            taxon_id = int(line_ls[1])
            lab_dic[taxon_id] = label_id
    return lab_dic


def vocab_dict(filename):
    """Turns the vocabulary into a dict={word: id}.
    """
    word_to_id = {}
    idx = 0
    with open(filename) as handle:
        for line in handle:
            word = line.rstrip()
            word_to_id[word] = idx
            idx += 1
    return word_to_id


def training_set_read_parser(rec, lab_dic):
    """Parses each training/eval read in biopython-parsed format.
    Species taxon ids are assumed to be available in read names.
    (E.g. for read with name >NC_018018.1|999|GCF_000265505.1-200000,
    999 is parsed as its species taxon id.)

    Returns:
        seq: string, the DNA sequences.
        label_id: int, zero-based id of each species for training.
    """
    seq = str(rec.seq)
    identifier = rec.id
    taxon_id = identifier.split('|')[1]
    taxon_id = int(taxon_id)
    label_id = lab_dic[taxon_id]
    return seq, label_id


def test_set_read_parser(rec):
    """Parses each test read in biopython-parsed format.
    A DNA string id is returned without its label.
    """
    seq = str(rec.seq)
    return seq


def kmer2index(k_mer, word_to_id):
    """Converts k-mer to index to the embedding layer"""
    if k_mer in word_to_id:
        idx = word_to_id[k_mer]
    elif forward2reverse(k_mer) in word_to_id:
        idx = word_to_id[forward2reverse(k_mer)]
    else:
        idx = word_to_id['<unk>']
    return idx


def seq2kmer(seq, k, word_to_id):
    """Converts a DNA sequence split into a list of k-mers.
    The sequences in one data set do not have to share the same length.
    Returns:
         kmer_array: a numpy array of corresponding k-mer indexes.
    """
    l = len(seq)
    kmer_list = []
    for i in range(0, l):
        if i + k >= l + 1:
            break
        k_mer = seq[i:i+k]
        idx = kmer2index(k_mer, word_to_id)
        kmer_list.append(idx)
    kmer_array = np.array(kmer_list)
    return kmer_array


def wrap_read(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def wrap_label(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def training_set_convert2tfrecord(input_seq, output_tfrec, kmer, vocab,
                                  label, seq_type):
    """Converts reads to tfrecord, and saves to output file.
    Args:
        input_seq: string, path to the input fasta or fastq file.
        output_tfrec: string, path to the output tfrecord file.
        kmer: int, size of k for reads splitting.
        vocab: string, path to the vocabulary file containing all k-mer tokens.
        label: string, path to the tab-delimited file mapping from zero-based
          label to species taxid.
        seq_type: string, reads format, should be fasta or fastq.

    """
    tf.logging.info("Parsing label")
    lab_dic = label_dict(label)
    tf.logging.info("Parsing vocabulary")
    word_to_dic = vocab_dict(vocab)
    with tf.python_io.TFRecordWriter(output_tfrec) as writer:
        with open(input_seq) as handle:
            for rec in SeqIO.parse(handle, seq_type):
                seq, label_id = training_set_read_parser(rec, lab_dic)
                kmer_array = seq2kmer(seq, kmer, word_to_dic)
                data = \
                        {
                            'read': wrap_read(kmer_array),
                            'label': wrap_label(label_id)
                        }
                feature = tf.train.Features(feature=data)
                example = tf.train.Example(features=feature)
                serialized = example.SerializeToString()
                writer.write(serialized)


def test_set_convert2tfrecord(input_seq, output_tfrec, kmer, vocab, seq_type):
    """Converts reads to tfrecord, and saves to output file.
    Args:
        input_seq: string, path to the input fasta or fastq file.
        output_tfrec: string, path to the output tfrecord file.
        kmer: int, size of k for reads splitting.
        vocab: string, path to the vocabulary file containing all k-mer tokens.
        seq_type: string, reads format, should be fasta or fastq.

    """
    tf.logging.info("Parsing vocabulary")
    word_to_dic = vocab_dict(vocab)
    with tf.python_io.TFRecordWriter(output_tfrec) as writer:
        with open(input_seq) as handle:
            for rec in SeqIO.parse(handle, seq_type):
                seq = test_set_read_parser(rec)
                kmer_array = seq2kmer(seq, kmer, word_to_dic)
                data = \
                        {
                            'read': wrap_read(kmer_array)
                        }
                feature = tf.train.Features(feature=data)
                example = tf.train.Example(features=feature)
                serialized = example.SerializeToString()
                writer.write(serialized)


def main(unused_argv):
    # checking files: vocab, label (for training/eval set), input_seq
    assert os.path.exists(FLAGS.vocab), (
        'Please provide the vocabulary file.')
    assert os.path.exists(FLAGS.input_seq), (
        'Please provide input fasta or fastq.')

    if FLAGS.is_train:
        assert os.path.exists(FLAGS.label), (
            'Please provide the label file for training/eval set.')
        tf.logging.info("Processing training/eval set")
        training_set_convert2tfrecord(FLAGS.input_seq, FLAGS.output_tfrec,
                                      FLAGS.kmer, FLAGS.vocab, FLAGS.label,
                                      FLAGS.seq_type)
    else:
        tf.logging.info("Processing test set")
        test_set_convert2tfrecord(FLAGS.input_seq, FLAGS.output_tfrec,
                                  FLAGS.kmer, FLAGS.vocab, FLAGS.seq_type)


def define_seq2tfrec_flags():
    flags.DEFINE_string(
        name="input_seq", short_name="seq", default="/tmp/input.fasta",
        help=flags_core.help_wrap(
            "Path to input reads"))
    flags.DEFINE_string(
        name="output_tfrec", short_name="tfrec", default="/tmp/output.tfrec",
        help=flags_core.help_wrap(
            "Path to output tfrecord"))
    flags.DEFINE_string(
        name="vocab", default="/tmp/tokens_12mer.txt",
        help=flags_core.help_wrap(
            "Path to the vocabulary file"))
    flags.DEFINE_string(
        name="label", default="/tmp/label2taxid.txt",
        help=flags_core.help_wrap(
            "Path to the label file"))
    flags.DEFINE_string(
        name="seq_type", default="fasta",
        help=flags_core.help_wrap(
            "Input format, fasta or fastq (default fasta)"))
    flags.DEFINE_integer(
        name="kmer", short_name="k", default=12,
        help=flags_core.help_wrap(
            "The size of k for reads splitting (default 12)"))
    flags.DEFINE_boolean(
        name="is_train", default=True,
        help=flags_core.help_wrap(
            "Whether processing training/eval set (default True)"))


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    define_seq2tfrec_flags()
    FLAGS = flags.FLAGS
    absl_app.run(main)