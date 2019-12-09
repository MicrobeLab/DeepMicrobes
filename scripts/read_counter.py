#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import argparse
import operator


def lab2name(label2name):
    label2name_dict = {}
    with open(label2name) as handle:
        for line in handle:
            line_ls = line.rstrip().split('\t')
            label2name_dict[line_ls[1]] = line_ls[0]
    return label2name_dict


def count_reads(prediction):
    label2count_dict = {}
    with open(prediction) as handle:
        for line in handle:
            line_ls = line.rstrip().split('\t')
            label = line_ls[0]
            if label in label2count_dict:
                label2count_dict[label] += 1
            else:
                label2count_dict[label] = 1
    return label2count_dict


def write_report(label2count_dict, output_name, label2name_dict):
    label2count_list = sorted(label2count_dict.items(), key=operator.itemgetter(1), reverse=True)
    with open(output_name, 'w') as handle:
        for label, count in label2count_list:
            name = label2name_dict[label]
            rec = '\t'.join([name, str(count)])
            handle.write(rec + '\n')
    return


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='prediction', type=str, help='/path/to/prediction.')
    parser.add_argument('-o', dest='output_name', type=str, help='/path/to/output.')
    parser.add_argument('-l', dest='label2name', type=str, help='/path/to/label2name.')

    args = parser.parse_args()

    label2name_dict = lab2name(args.label2name)
    label2count_dict = count_reads(args.prediction)
    write_report(label2count_dict, args.output_name, label2name_dict)

    return


if __name__ == '__main__':
    main()

