from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import argparse
import sys
from Bio import SeqIO


def sequence_from_text_file(sequence_file):
    with open(sequence_file) as handle:
        sequence = handle.read().rstrip()
    return sequence


def sequence_from_fasta_file(sequence_file, seq_idx):
    count = 0
    sequence = None
    with open(sequence_file) as handle:
        for rec in SeqIO.parse(handle, 'fasta'):
            seq = str(rec.seq)
            if count == seq_idx:
                sequence = seq
            if len(seq) != 100:
                print('warning')
            count += 1
    return sequence


def softmax(x):
    return np.exp(x)/np.sum(np.exp(x), axis=0)


def normalize_attention(attention_matrix, seq_idx):
    attention_matrix = np.load(attention_matrix)  # [batch=1, len-k+1, row=30]
    attention_matrix = np.sum(attention_matrix, axis=2)[seq_idx]  # [len-k+1]
    return attention_matrix


def assign_attention_to_bases(attention_matrix, kmer_length, seq_idx):
    attention_matrix = normalize_attention(attention_matrix, seq_idx)
    attention_length = len(attention_matrix)
    dna_length = attention_length - 1 + kmer_length
    dna_attention = np.zeros(dna_length)
    for i in range(attention_length):
        a_i = attention_matrix[i]
        if a_i < 0.0:
            a_i = 0
        for j in range(i, i + kmer_length):
            dna_attention[j] += a_i
    return 1 - softmax(dna_attention) * 5


def assign_attention_to_base_start(attention_matrix, kmer_length, seq_idx):
    attention_matrix = normalize_attention(attention_matrix, seq_idx)
    attention_length = len(attention_matrix)
    dna_length = attention_length - 1 + kmer_length
    dna_attention = np.zeros(dna_length)
    for i in range(attention_length):
        a_i = attention_matrix[i]
        if a_i < 0.0:
            a_i = 0
        dna_attention[i + 1] = a_i
    return 1 - dna_attention


def format_html(name_prefix, sequence, attention):
    # Modified from implementation by Diego Antognini available at:
    # https://github.com/Diego999/SelfSent
    with open(name_prefix + '.html', 'w') as handle:
        handle.write('<!DOCTYPE html>\n<html>\n<head>\n')
        handle.write('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>\n')
        handle.write('<script>\n')
        handle.write('window.onload=function(){\n')
        handle.write('var words = [{\n')
        handle.write("'word': " + "'" + sequence[0] + "'" + ",\n'attention': " + str(round(attention[0], ndigits=2)))
        handle.write('\n')
        for i in range(1, len(sequence)):
            handle.write('}, {\n')
            handle.write("'word': " + "'" + sequence[i] + "'" + ",\n'attention': " + str(round(attention[i], ndigits=2)))
            handle.write('\n')
        handle.write('}];\n\n')
        handle.write("$('#text').html($.map(words, function(w) {\n")
        handle.write("  return '<span style=\"background-color:hsl(320,100%,' + (w.attention * 50 + 50) + '%)\">' + w.word + ' </span>'\n")
        handle.write('}))\n}\n</script>\n</head>\n<body>\n\n')
        handle.write('<div id="text">text goes here</div>\n\n')
        handle.write('</body>\n</html>\n')
    return


def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='sequence_file', type=str, help='/path/to/DNA_sequences.')
    parser.add_argument('-a', dest='attention_matrix', type=str, help='/path/to/attention_matrix.')
    parser.add_argument('-o', dest='output_prefix', type=str, default='test', help='Filename of output html.')
    parser.add_argument('-k', dest='kmer_length', type=int, default=12, help='Length of k-mers')
    parser.add_argument('-m', dest='mode', type=str, default='even', help='Mode')
    parser.add_argument('-i', dest='seq_idx', type=int, default=0, help='Index of sequence.')

    args = parser.parse_args()

    sequence_file = args.sequence_file
    attention_matrix = args.attention_matrix
    output_prefix = args.output_prefix
    kmer_length = args.kmer_length
    mode = args.mode
    seq_idx = args.seq_idx

    sequence = sequence_from_fasta_file(sequence_file, seq_idx)
    if mode == 'even':
        attention = assign_attention_to_bases(attention_matrix, kmer_length, seq_idx)
    elif mode == 'start':
        attention = assign_attention_to_base_start(attention_matrix, kmer_length, seq_idx)
    else:
        attention = None
    # print(attention)
    format_html(output_prefix, sequence, attention)
    

if __name__ == '__main__':
    main(sys.argv)