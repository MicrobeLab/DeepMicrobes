from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os


def label_one_genome(input_name, label, out_path):
    if out_path is None:
        out_path = os.getcwd()
    output_name = os.path.join(out_path, 'label_' + input_name)
    with open(output_name, 'w') as handle_out:
        with open(input_name, 'r') as handle_in:
            for line in handle_in:
                if line.startswith('>'):
                    line = '>' + 'label|' + label + '|' + line[1:]
                handle_out.write(line)
    return


def label_all_genomes(map_file, out_path):
    with open(map_file, 'r') as handle_map:
        for line in handle_map:
            line_ls = line.rstrip().split('\t')
            input_name = line_ls[0]
            label = line_ls[1]
            label_one_genome(input_name, label, out_path)
    return


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', dest='map_file', type=str,
                        help='/path/to/map_file.txt')
    parser.add_argument('-o', dest='out_path', type=str, default=None,
                        help='/path/to/output_dir')

    args = parser.parse_args()
    map_file = args.map_file
    out_path = args.out_path

    label_all_genomes(map_file, out_path)

    return


if __name__ == '__main__':
    main()

