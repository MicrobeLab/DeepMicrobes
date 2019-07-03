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


def tax2name(taxid2name):
    taxid2name_dict = {}
    with open(taxid2name) as handle:
        for line in handle:
            line_ls = line.rstrip().split('\t')
            taxid2name_dict[line_ls[1]] = line_ls[0]
    return taxid2name_dict


def count_reads(reads_prediction, min_reads_prob):
    taxon2count_dict = {}
    taxon2prob_dict = {}
    with open(reads_prediction) as handle:
        for line in handle:
            line_ls = line.rstrip().split('\t')
            taxon = line_ls[0]
            prob = float(line_ls[1])
            if prob < min_reads_prob:
                continue
            if taxon in taxon2count_dict:
                taxon2count_dict[taxon] += 1
                taxon2prob_dict[taxon] += prob
            else:
                taxon2count_dict[taxon] = 1
                taxon2prob_dict[taxon] = prob
    for taxon in taxon2count_dict:
        count = taxon2count_dict[taxon]
        taxon2prob_dict[taxon] = round(taxon2prob_dict[taxon]/count, ndigits=2)

    return taxon2count_dict, taxon2prob_dict


def filter_taxon(min_count, min_prob, taxon2count_dict, taxon2prob_dict):
    for taxon in taxon2count_dict:
        count = taxon2count_dict[taxon]
        if count < min_count or taxon2prob_dict[taxon] < min_prob:
            taxon2count_dict.pop(taxon)
            taxon2prob_dict.pop(taxon)
    return taxon2count_dict, taxon2prob_dict


def write_report(taxon2count_dict, taxon2prob_dict, output_profile,
                 label2name_dict=None, taxid2name_dict=None, translated=True):
    taxon2count_list = sorted(taxon2count_dict.items(), key=operator.itemgetter(1), reverse=True)
    with open(output_profile, 'w') as handle:
        title = '\t'.join(['Name', 'Count', 'Confidence'])
        handle.write(title + '\n')
        for taxon, count in taxon2count_list:
            if translated:
                name = taxid2name_dict[taxon]
            else:
                name = label2name_dict[taxon]
            rec = '\t'.join([name, str(count), str(taxon2prob_dict[taxon])])
            handle.write(rec + '\n')
    return


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='reads_prediction', type=str, help='/path/to/reads_prediction.')
    parser.add_argument('-o', dest='output_profile', type=str, help='/path/to/output_profile.')
    parser.add_argument('-l', dest='label2name', type=str, default=None, help='/path/to/label2name.')
    parser.add_argument('-t', dest='taxid2name', type=str, default=None, help='/path/to/taxid2name.')
    parser.add_argument('-c', dest='min_count', type=int, default=0, help='Minimum count of presence taxon.')
    parser.add_argument('-p', dest='min_prob', type=float, default=50, help='Minimum prob of presence taxon.')
    parser.add_argument('-pr', dest='min_reads_prob', type=float, default=50, help='Minimum prob of reads.')
    parser.add_argument('-tr', dest='translated', type=bool, default=False,
                        help='Whether labels were translated to taxids')

    args = parser.parse_args()
    reads_prediction = args.reads_prediction
    output_profile = args.output_profile
    label2name = args.label2name
    taxid2name = args.taxid2name
    min_count = args.min_count
    min_prob = args.min_prob
    translated = args.translated
    min_reads_prob = args.min_reads_prob

    taxon2count_dict, taxon2prob_dict = count_reads(reads_prediction, min_reads_prob)
    taxon2count_dict, taxon2prob_dict = filter_taxon(min_count, min_prob, taxon2count_dict, taxon2prob_dict)
    if translated:
        taxid2name_dict = tax2name(taxid2name)
        write_report(taxon2count_dict, taxon2prob_dict, output_profile,
                     taxid2name_dict=taxid2name_dict, translated=True)
    else:
        label2name_dict = lab2name(label2name)
        write_report(taxon2count_dict, taxon2prob_dict, output_profile,
                     label2name_dict=label2name_dict, translated=False)

    return


if __name__ == '__main__':
    main()
