from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from absl import flags
from absl import app as absl_app

import numpy as np
import tensorflow as tf

from models import embed_pool, embed_cnn, cnn_lstm, resnet_cnn, \
    embed_lstm, embed_lstm_attention, seq2species

from models.input_pipeline import input_function_train_kmer, input_function_train_one_hot, \
    input_function_predict_kmer, input_function_predict_one_hot, \
    input_function_train_kmer_pad_to_fixed_len, input_function_predict_kmer_pad_to_fixed_len

from models.define_flags import universal_flags, model_specific_flags_embed_cnn, \
    model_specific_flags_embed_lstm, flags_of_mode

from models.format_prediction import prob2npy, top_n_class, paired_report, \
    prob2npy_paired, single_report

from utils.logs import hooks_helper
from utils.logs import logger

# import sys
# sys.path.append('models')


def config(model_name, params):
    if model_name == 'embed_pool':
        model = embed_pool.EmbedPool(num_classes=params['num_classes'],
                                     vocab_size=params['vocab_size'],
                                     embedding_dim=params['embedding_dim'],
                                     mlp_dim=params['mlp_dim'],
                                     kmer=params['kmer'],
                                     max_len=params['max_len'])
    elif model_name == 'embed_cnn':
        model = embed_cnn.EmbedCNN(num_classes=params['num_classes'],
                                   vocab_size=params['vocab_size'],
                                   embedding_dim=params['embedding_dim'],
                                   mlp_dim=params['mlp_dim'],
                                   cnn_filter_sizes=list(map(int, params['cnn_filter_sizes'].split(","))),
                                   cnn_num_filters=params['cnn_num_filters'],
                                   kmer=params['kmer'],
                                   max_len=params['max_len'])
    elif model_name == 'embed_cnn_no_pool':
        model = embed_cnn.EmbedCNNnoPool(num_classes=params['num_classes'],
                                         vocab_size=params['vocab_size'],
                                         embedding_dim=params['embedding_dim'],
                                         mlp_dim=params['mlp_dim'],
                                         cnn_filter_sizes=list(map(int, params['cnn_filter_sizes'].split(","))),
                                         cnn_num_filters=params['cnn_num_filters'],
                                         kmer=params['kmer'],
                                         max_len=params['max_len'])
    elif model_name == 'embed_lstm':
        model = embed_lstm.EmbedLSTM(num_classes=params['num_classes'],
                                     vocab_size=params['vocab_size'],
                                     embedding_dim=params['embedding_dim'],
                                     mlp_dim=params['mlp_dim'],
                                     lstm_dim=params['lstm_dim'],
                                     pooling_type=params['pooling_type'],
                                     kmer=params['kmer'],
                                     max_len=params['max_len'])
    elif model_name == 'cnn_lstm':
        model = cnn_lstm.ConvLSTM(num_classes=params['num_classes'],
                                  max_len=params['max_len'])
    elif model_name == 'cnn_2lstm':
        model = cnn_lstm.Conv2LSTM(num_classes=params['num_classes'],
                                   max_len=params['max_len'])
    elif model_name == 'deep_cnn':
        model = resnet_cnn.DeepCNN(num_classes=params['num_classes'],
                                   max_len=params['max_len'])
    elif model_name == 'deep_cnn_13layer':
        model = resnet_cnn.DeepCNN13(num_classes=params['num_classes'],
                                     max_len=params['max_len'])
    elif model_name == 'deep_cnn_9layer':
        model = resnet_cnn.DeepCNN9(num_classes=params['num_classes'],
                                    max_len=params['max_len'])
    elif model_name == 'seq2species':
        model = seq2species.Seq2species(num_classes=params['num_classes'],
                                        max_len=params['max_len'])
    else:
        model = embed_lstm_attention.EmbedAttention(num_classes=params['num_classes'],
                                                    vocab_size=params['vocab_size'],
                                                    embedding_dim=params['embedding_dim'],
                                                    mlp_dim=params['mlp_dim'],
                                                    lstm_dim=params['lstm_dim'],
                                                    row=params['row'],
                                                    da=params['da'],
                                                    keep_prob=params['keep_prob'])
    return model


def model_fn(features, labels, mode, params):
    model = config(flags.FLAGS.model_name, params)
    logits = model(features)

    predictions = {
        'classes': tf.argmax(logits, axis=1),
        'probabilities': tf.nn.softmax(logits)
    }

    if mode == tf.estimator.ModeKeys.PREDICT:
        # Return the predictions and the specification for serving a SavedModel
        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions=predictions,
            export_outputs={
                'predict': tf.estimator.export.PredictOutput(predictions)
            })

    loss = tf.losses.sparse_softmax_cross_entropy(
        logits=logits, labels=labels)

    # Create a tensor named cross_entropy for logging purposes.
    tf.identity(loss, name='cross_entropy')
    tf.summary.scalar('cross_entropy', loss)

    if mode == tf.estimator.ModeKeys.TRAIN:
        global_step = tf.train.get_or_create_global_step()

        learning_rate = tf.train.exponential_decay(params['lr'], global_step, 400000,
                                                   params['lr_decay'], staircase=False)

        # Create a tensor named learning_rate for logging purposes
        tf.identity(learning_rate, name='learning_rate')
        tf.summary.scalar('learning_rate', learning_rate)

        optimizer = tf.train.AdamOptimizer(learning_rate)
        minimize_op = optimizer.minimize(loss, global_step)
        update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        train_op = tf.group(minimize_op, update_ops)
    else:
        train_op = None

    accuracy = tf.metrics.accuracy(labels, predictions['classes'])

    metrics = {'accuracy': accuracy}

    # Create a tensor named train_accuracy for logging purposes
    tf.identity(accuracy[1], name='train_accuracy')
    tf.summary.scalar('train_accuracy', accuracy[1])

    return tf.estimator.EstimatorSpec(
        mode=mode,
        predictions=predictions,
        loss=loss,
        train_op=train_op,
        eval_metric_ops=metrics)


def train(flags_obj, model_function, dataset_name):
    run_config = tf.estimator.RunConfig(save_checkpoints_steps=100000, keep_checkpoint_max=1000)

    classifier = tf.estimator.Estimator(
        model_fn=model_function, model_dir=flags_obj.model_dir, config=run_config,
        params={
            'num_classes': flags_obj.num_classes,
            'vocab_size': flags_obj.vocab_size,
            'embedding_dim': flags_obj.embedding_dim,
            'mlp_dim': flags_obj.mlp_dim,
            'kmer': flags_obj.kmer,
            'max_len': flags_obj.max_len,
            'lr': flags_obj.lr,
            'lr_decay': flags_obj.lr_decay,
            'cnn_num_filters': flags_obj.cnn_num_filters,
            'cnn_filter_sizes': flags_obj.cnn_filter_sizes,
            'lstm_dim': flags_obj.lstm_dim,
            'pooling_type': flags_obj.pooling_type,
            'row': flags_obj.row,
            'da': flags_obj.da,
            'keep_prob': flags_obj.keep_prob
        })

    run_params = {
        'batch_size': flags_obj.batch_size,
        'train_epochs': flags_obj.train_epochs,
    }
    benchmark_logger = logger.config_benchmark_logger(flags_obj)
    benchmark_logger.log_run_info('model', dataset_name, run_params)

    train_hooks = hooks_helper.get_train_hooks(
        flags_obj.hooks,
        batch_size=flags_obj.batch_size)

    def input_fn_train():
        if flags_obj.encode_method == 'kmer':
            input_fn = input_function_train_kmer(
                flags_obj.input_tfrec,
                flags_obj.train_epochs, flags_obj.batch_size,
                flags_obj.cpus
            )
            if flags_obj.model_name in ['embed_pool', 'embed_cnn', 'embed_lstm',
                                        'embed_cnn_no_pool']:
                input_fn = input_function_train_kmer_pad_to_fixed_len(
                    flags_obj.input_tfrec,
                    flags_obj.train_epochs, flags_obj.batch_size,
                    flags_obj.cpus, flags_obj.max_len, flags_obj.kmer
                )
        else:
            input_fn = input_function_train_one_hot(
                flags_obj.input_tfrec,
                flags_obj.train_epochs, flags_obj.batch_size,
                flags_obj.cpus, flags_obj.max_len
            )

        return input_fn

    classifier.train(input_fn=input_fn_train, hooks=train_hooks)


def evaluate(flags_obj, model_function):

    classifier = tf.estimator.Estimator(
        model_fn=model_function, model_dir=flags_obj.model_dir,
        params={
            'num_classes': flags_obj.num_classes,
            'vocab_size': flags_obj.vocab_size,
            'embedding_dim': flags_obj.embedding_dim,
            'mlp_dim': flags_obj.mlp_dim,
            'kmer': flags_obj.kmer,
            'max_len': flags_obj.max_len,
            'lr': flags_obj.lr,
            'lr_decay': flags_obj.lr_decay,
            'cnn_num_filters': flags_obj.cnn_num_filters,
            'cnn_filter_sizes': flags_obj.cnn_filter_sizes,
            'lstm_dim': flags_obj.lstm_dim,
            'pooling_type': flags_obj.pooling_type,
            'row': flags_obj.row,
            'da': flags_obj.da,
            'keep_prob': flags_obj.keep_prob
        })

    def input_fn_eval():
        if flags_obj.encode_method == 'kmer':
            input_fn = input_function_train_kmer(
                flags_obj.input_tfrec,
                1, flags_obj.batch_size,
                flags_obj.cpus
            )
            if flags_obj.model_name in ['embed_pool', 'embed_cnn', 'embed_lstm',
                                        'embed_cnn_no_pool']:
                input_fn = input_function_train_kmer_pad_to_fixed_len(
                    flags_obj.input_tfrec,
                    1, flags_obj.batch_size,
                    flags_obj.cpus, flags_obj.max_len, flags_obj.kmer
                )
        else:
            input_fn = input_function_train_one_hot(
                flags_obj.input_tfrec,
                1, flags_obj.batch_size,
                flags_obj.cpus, flags_obj.max_len
            )

        return input_fn

    classifier.evaluate(input_fn=input_fn_eval)


def predict(flags_obj, model_function):

    classifier = tf.estimator.Estimator(
        model_fn=model_function, model_dir=flags_obj.model_dir,
        params={
            'num_classes': flags_obj.num_classes,
            'vocab_size': flags_obj.vocab_size,
            'embedding_dim': flags_obj.embedding_dim,
            'mlp_dim': flags_obj.mlp_dim,
            'kmer': flags_obj.kmer,
            'max_len': flags_obj.max_len,
            'lr': flags_obj.lr,
            'lr_decay': flags_obj.lr_decay,
            'cnn_num_filters': flags_obj.cnn_num_filters,
            'cnn_filter_sizes': flags_obj.cnn_filter_sizes,
            'lstm_dim': flags_obj.lstm_dim,
            'pooling_type': flags_obj.pooling_type,
            'row': flags_obj.row,
            'da': flags_obj.da,
            'keep_prob': flags_obj.keep_prob
        })

    def input_fn_predict():
        if flags_obj.encode_method == 'kmer':
            input_fn = input_function_predict_kmer(
                flags_obj.input_tfrec,
                flags_obj.batch_size,
                flags_obj.cpus
            )
            if flags_obj.model_name in ['embed_pool', 'embed_cnn', 'embed_lstm',
                                        'embed_cnn_no_pool']:
                input_fn = input_function_predict_kmer_pad_to_fixed_len(
                    flags_obj.input_tfrec,
                    flags_obj.batch_size,
                    flags_obj.cpus,
                    flags_obj.max_len,
                    flags_obj.kmer
                )
        else:
            input_fn = input_function_predict_one_hot(
                flags_obj.input_tfrec,
                flags_obj.batch_size,
                flags_obj.cpus,
                flags_obj.max_len
            )
        return input_fn

    return classifier.predict(input_fn=input_fn_predict, yield_single_examples=False)


def main(_):
    if flags.FLAGS.running_mode == 'eval':
        evaluate(flags.FLAGS, model_fn)
    elif flags.FLAGS.running_mode == 'predict_prob':
        predict_out = predict(flags.FLAGS, model_fn)
        prob_matrix = prob2npy(
            predict_out,
            flags.FLAGS.num_classes,
            flags.FLAGS.strands_average)
        np.save(flags.FLAGS.pred_out, prob_matrix)
    elif flags.FLAGS.running_mode == 'predict_top_n':
        predict_out = predict(flags.FLAGS, model_fn)
        top_n_indexes, top_n_probs = top_n_class(
            predict_out,
            flags.FLAGS.num_classes,
            flags.FLAGS.top_n_class,
            flags.FLAGS.strands_average)
        np.savetxt(flags.FLAGS.pred_out+'.category.txt', top_n_indexes, fmt='%d', delimiter='\t')
        np.savetxt(flags.FLAGS.pred_out+'.prob.txt', top_n_probs, fmt='%.2f', delimiter='\t')
    elif flags.FLAGS.running_mode == 'predict_single_class':
        predict_out = predict(flags.FLAGS, model_fn)
        classes, probs = single_report(predict_out,
                                       flags.FLAGS.num_classes,
                                       flags.FLAGS.label_file,
                                       flags.FLAGS.translate,
                                       flags.FLAGS.strands_average)
        np.savetxt(flags.FLAGS.pred_out + '.category_single.txt', classes, fmt='%d', delimiter='\t')
        np.savetxt(flags.FLAGS.pred_out + '.prob_single.txt', probs, fmt='%.2f', delimiter='\t')
    elif flags.FLAGS.running_mode == 'predict_paired_class':
        predict_out = predict(flags.FLAGS, model_fn)
        classes, probs = paired_report(predict_out,
                                       flags.FLAGS.num_classes,
                                       flags.FLAGS.label_file,
                                       flags.FLAGS.translate)
        np.savetxt(flags.FLAGS.pred_out + '.category_paired.txt', classes, fmt='%d', delimiter='\t')
        np.savetxt(flags.FLAGS.pred_out + '.prob_paired.txt', probs, fmt='%.2f', delimiter='\t')
    elif flags.FLAGS.running_mode == 'predict_paired_prob':
        predict_out = predict(flags.FLAGS, model_fn)
        prob_matrix = prob2npy_paired(predict_out,
                                      flags.FLAGS.num_classes)
        np.save(flags.FLAGS.pred_out, prob_matrix)
    else:
        train(flags.FLAGS, model_fn, 'dataset_name')

if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    universal_flags()
    model_specific_flags_embed_cnn()
    model_specific_flags_embed_lstm()
    flags_of_mode()
    absl_app.run(main)

