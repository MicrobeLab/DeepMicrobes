#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import random
from Bio import SeqIO


def trim_one_seq(seq, min_trim=0, max_trim=75, ori_seq_len=150):
    # generate variable-length DNA between [L-max_trim, L-min_trim]
    trim_num = random.randint(min_trim, max_trim)
    trimmed_seq = str(seq).rstrip()[0:(ori_seq_len-trim_num)] + '\n'
    return trimmed_seq


def trim_one_file(raw_file, out_file, file_type='fastq',
                  min_trim=0, max_trim=75, ori_seq_len=150):
    with open(out_file, 'w') as handle_out:
        with open(raw_file, 'r') as handle_raw:
            for rec in SeqIO.parse(handle_raw, file_type):
                trimmed_seq = trim_one_seq(rec.seq, min_trim, max_trim,
                                           ori_seq_len)
                seq_name = rec.id + '\n'
                handle_out.write('>' + seq_name)
                handle_out.write(trimmed_seq)
    return


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='raw_file', type=str,
                        help='/path/to/input_fastq')
    parser.add_argument('-o', dest='out_file', type=str,
                        help='/path/to/output_fasta')
    parser.add_argument('-f', dest='file_type', type=str, default='fastq',
                        help='input file type: fasta/fastq')
    parser.add_argument('-min', dest='min_trim', type=int, default=0,
                        help='min # of trimmed bases')
    parser.add_argument('-max', dest='max_trim', type=int, default=75,
                        help='max # of trimmed bases')
    parser.add_argument('-l', dest='ori_seq_len', type=int, default=150,
                        help='length of raw sequences')

    args = parser.parse_args()
    raw_file = args.raw_file
    out_file = args.out_file
    file_type = args.file_type
    min_trim = args.min_trim
    max_trim = args.max_trim
    ori_seq_len = args.ori_seq_len

    trim_one_file(raw_file, out_file, file_type, min_trim, max_trim, ori_seq_len)

    return


if __name__ == '__main__':
    main()
