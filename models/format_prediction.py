from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np


def average_double_strands(prob_matrix, num_classes):
    prob_matrix = np.mean(np.reshape(prob_matrix, (-1, 2, num_classes)), axis=1)
    return prob_matrix


def average_paired_end(prob_matrix, num_classes):
    prob_matrix = np.mean(np.reshape(prob_matrix, (-1, 4, num_classes)), axis=1)
    return prob_matrix


def index2taxid(label_file):
    """Turns the label info into a dict={label: taxid}."""
    lab_dic = {}
    with open(label_file) as handle:
        for line in handle:
            line_ls = line.rstrip().split('\t')
            label_id = int(line_ls[0])
            taxon_id = int(line_ls[1])
            lab_dic[label_id] = taxon_id
    return lab_dic


def prob2npy(prediction_generator, num_classes, strands_average=True):
    probs = []
    while True:
        try:
            batch_prob = next(prediction_generator)['probabilities']
            if strands_average:
                batch_prob = average_double_strands(batch_prob, num_classes)
            probs.append(batch_prob)
        except StopIteration:
            print("Prediction finished.")
            break
    probs = np.concatenate(probs)
    return probs


def prob2npy_paired(prediction_generator, num_classes):
    probs = []
    while True:
        try:
            batch_prob = next(prediction_generator)['probabilities']
            batch_prob = average_paired_end(batch_prob, num_classes)
            probs.append(batch_prob)
        except StopIteration:
            print("Prediction finished.")
            break
    probs = np.concatenate(probs)
    return probs


def top_n_class(prediction_generator, num_classes, top_n, strands_average=True):
    top_n_index_list = []
    top_n_prob_list = []
    while True:
        try:
            batch_prob = next(prediction_generator)['probabilities']
            if strands_average:
                batch_prob = average_double_strands(batch_prob, num_classes)
            for i in range(batch_prob.shape[0]):
                prob_vector = batch_prob[i]
                top_n_index = prob_vector.argsort()[-top_n:][::-1]
                top_n_index_list.append(np.expand_dims(top_n_index, axis=0))
                top_n_prob = prob_vector[top_n_index]
                top_n_prob_list.append(np.expand_dims(top_n_prob, axis=0))
        except StopIteration:
            print("Prediction finished.")
            break
    return np.concatenate(top_n_index_list), np.concatenate(top_n_prob_list)*100


def paired_report(prediction_generator, num_classes, label_file, translate=True):
    class_list = []
    max_prob_list = []
    if translate:
        lab_dic = index2taxid(label_file)
    else:
        lab_dic = None
    while True:
        try:
            batch_prob = next(prediction_generator)['probabilities']
            batch_prob = average_paired_end(batch_prob, num_classes)
            indexes = np.argmax(batch_prob, axis=1)
            if translate:
                for i in range(len(indexes)):
                    indexes[i] = lab_dic[indexes[i]]
            class_list.append(indexes)
            max_prob_list.append(np.max(batch_prob, axis=1))
        except StopIteration:
            print("Prediction finished.")
            break
    return np.concatenate(class_list), np.concatenate(max_prob_list)*100


def single_report(prediction_generator, num_classes, label_file,
                  translate=True, strands_average=True):
    class_list = []
    max_prob_list = []
    if translate:
        lab_dic = index2taxid(label_file)
    else:
        lab_dic = None
    while True:
        try:
            batch_prob = next(prediction_generator)['probabilities']
            if strands_average:
                batch_prob = average_double_strands(batch_prob, num_classes)
            indexes = np.argmax(batch_prob, axis=1)
            if translate:
                for i in range(len(indexes)):
                    indexes[i] = lab_dic[indexes[i]]
            class_list.append(indexes)
            max_prob_list.append(np.max(batch_prob, axis=1))
        except StopIteration:
            print("Prediction finished.")
            break
        return np.concatenate(class_list), np.concatenate(max_prob_list) * 100

