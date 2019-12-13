# How to make predictions on a metagenome dataset

This tutorial assumes that fastq/fasta files have been converted to [TFRecord](https://github.com/MicrobeLab/DeepMicrobes/blob/master/document/tfrecord.md).

To get a full list of options for `DeepMicrobes.py`:

```sh
DeepMicrobes.py --helpfull
```

The shell scripts used to make predictions with all tested DNNs in the paper can be found in [pipelines](https://github.com/MicrobeLab/DeepMicrobes/tree/master/pipelines). 
In these scripts we use the `--model_name` option to tell `DeepMicrobes.py` which DNN architecture we would like to use. <br>
The scripts of models called by `DeepMicrobes.py` are indicated in square brackets below.

<b>The final best DNN:</b>
* `attention`: Embed + LSTM + Attention (DeepMicrobes) [./models/embed_lstm_attention.py]

<b>Other tested DNNs:</b>
* `deep_cnn`: ResNet-like CNN [./models/resnet_cnn.py]
* `cnn_lstm`: CNN + LSTM [./models/cnn_lstm.py]
* `seq2species`: Seq2species [./models/seq2species.py]
* `embed_pool`: Embed + Pool [./models/embed_pool.py]
* `embed_cnn`: Embed + CNN [./models/embed_cnn.py]
* `embed_lstm`: Embed + LSTM [./models/embed_lstm.py]

## Classifying reads using DeepMicrobes

To make prediction on a metagenome dataset (referred to as `sample.tfrec`) using DeepMicrobes :
```sh
predict_DeepMicrobes.sh -i sample.tfrec -b 8192 -l species -p 8 -m model_dir -o prefix 
```

Arguments: <br>
* `-i` TFRecord input containing interleaved paired-end reads <br>
* `-m` Dictionary containing model weights (should match the taxonomic level) <br>
* `-o` Output prefix <br>
* `-b` (Optional) Batch size (a multiple of 4) (default: 8192) <br>
* `-l` (Optional) Taxonomic level, species/genus (should match the weights) (default: species) <br>
* `-p` (Optional) Number of parallel calls for input preparation (default: 8) <br>


<b>Note</b>: The model classifies sequences faster using a larger batch size. 
We recommend users to try different values and select the largest batch size that fits into memory. 

The script takes as input a TFRecord dataset and generates a tab-delimited output file containing predictions made on each pair of reads. 
* 1st column: category labels (integer)
* 2nd column: confidence score (decimal)

The tab-delimited file can then be used to generate a species/genus profile (see [next tutorial](https://github.com/MicrobeLab/DeepMicrobes/blob/master/document/profile.md)).



