from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from absl import flags
from utils.flags import core as flags_core


def universal_flags():
    flags_core.define_base()

    flags.DEFINE_integer(
        name='num_classes', default=2505,
        help=flags_core.help_wrap(
            'Number of species to classify.'))

    flags.DEFINE_integer(
        name='vocab_size', default=8390658,
        help=flags_core.help_wrap(
            'Number of k-mers in the vocabulary.'))

    flags.DEFINE_integer(
        name='embedding_dim', default=100,
        help=flags_core.help_wrap(
            'Dimension of embedding layer.'))

    flags.DEFINE_integer(
        name='mlp_dim', default=3000,
        help=flags_core.help_wrap(
            'Dimension of MLP.'))

    flags.DEFINE_integer(
        name='max_len', default=150,
        help=flags_core.help_wrap(
            'Max length of sequences.'))

    flags.DEFINE_integer(
        name='kmer', default=12,
        help=flags_core.help_wrap(
            'Length of k-mers.'))

    flags.DEFINE_integer(
        name='cpus', default=8,
        help=flags_core.help_wrap(
            'Number of cpus for input pipeline.'))

    flags.DEFINE_float(
        name='lr', default=0.001,
        help=flags_core.help_wrap(
            'Learning rate.'))

    flags.DEFINE_float(
        name='lr_decay', default=0.05,
        help=flags_core.help_wrap(
            'Learning rate decay.'))

    flags.DEFINE_float(
        name='keep_prob', default=1.0,
        help=flags_core.help_wrap(
            'Probability that an element is kept for dropout layers.'))

    flags.DEFINE_string(
        name='input_tfrec', default='/tmp/input.tfrec',
        help=flags_core.help_wrap(
            'Filename of training set.'))

    flags.DEFINE_string(
        name='model_name', default='attention',
        help=flags_core.help_wrap(
            'Choose a model.'))

    flags.DEFINE_string(
        name='encode_method', default='kmer',
        help=flags_core.help_wrap(
            'One of kmer/one_hot.'))


def model_specific_flags_embed_cnn():

    flags.DEFINE_string(
        name="cnn_filter_sizes", default="3,4,5",
        help=flags_core.help_wrap(
            "Comma-separated filter sizes (default: '3,4,5')"))

    flags.DEFINE_integer(
        name="cnn_num_filters", default=128,
        help=flags_core.help_wrap(
            "Number of filters per filter size (default: 128)"))


def model_specific_flags_embed_lstm():

    flags.DEFINE_integer(
        name="lstm_dim", default=300,
        help=flags_core.help_wrap(
            "Dimension of one direction of biLSTM (default: 300)"))

    flags.DEFINE_integer(
        name='da', default=350,
        help=flags_core.help_wrap(
            'Da.'))

    flags.DEFINE_integer(
        name='row', default=30,
        help=flags_core.help_wrap(
            'Number of rows of embedding matrix.'))

    flags.DEFINE_string(
        name="pooling_type", default='concat',
        help=flags_core.help_wrap(
            "Type of pooling: avg/max/concat (default: concat)"))


def flags_of_mode():

    flags.DEFINE_string(
        name="running_mode", default='train',
        help=flags_core.help_wrap(
            "One of: train/eval/predict_prob/predict_class/predict_paired_prob/predict_paired_class (default: train)"))

    flags.DEFINE_string(
        name="pred_out", default='/tmp/pred_out',
        help=flags_core.help_wrap(
            "/path/to/prediction/output"))

    flags.DEFINE_boolean(
        name="strands_average", default=True,
        help=flags_core.help_wrap(
            "Whether tfrec contains interleaved double strands (default: True)"))

    flags.DEFINE_integer(
        name="top_n_class", default=3,
        help=flags_core.help_wrap(
            "Output category indexes and probabilities for top n classes (default: 3)"))

    flags.DEFINE_string(
        name="label_file", default='/tmp/label2taxid.txt',
        help=flags_core.help_wrap(
            "File mapping from label to taxid (required if translate=True)"))

    flags.DEFINE_boolean(
        name="translate", default=True,
        help=flags_core.help_wrap(
            "Whether output taxid instead of label."))



