# How to convert fastq/fasta sequences to TFRecord

We provide the wrapper scripts that convert fastq/fasta sequences to TFRecord for training and prediction, respectively.
DeepMicrobes and the other embedding based DNNs use `kmer` representation. 
Other tested architectures including the convolutional model, the hybrid model, and seq2species use `onehot` representation.

<br>

## Training

The following steps are required to process the sequences in training sets before loading them into the model:
* Shuffle the sequences
* Split the large dataset to multiple small files (for acceleration)
* Convert the fasta sequences to TFRecord

<br>

<b>To convert fasta to TFRecord for training:</b>

```sh
tfrec_train_kmer.sh -i train.fa -v /path/to/vocab/tokens_merged_12mers.txt -d /path/to/DeepMicrobes/scripts -o output_dir -s 20480000 -k 12
```

Arguments: <br>
`-i` Fasta file of training set <br>
`-v` Absolute path to the vocabulary file (path/to/vocab/tokens_merged_12mers.txt) <br>
`-d` Absolute path of directory containing scripts (/path/to/DeepMicrobes/scripts) <br>
`-o` (Optional) Output dictionary containing converted TFRecord (default: tfrec) <br>
`-s` (Optional) Number of sequences per file for splitting (default: 20480000) <br>
`-k` (Optional) k-mer length (default: 12)

The converted TFRecord will be stored in `output_dir/train.tfrec`. <br>
<b>NOTE</b>: The script parses category labels from sequence IDs which should be start with `prefix|label` (e.g., >this_is_prefix|0). 
Suppose we 100 categories, we should assign a non-redundant integer label between 0-99 to each category.
The label is taken as ground truth during training and not required during prediction.
Each subset files are processed with one CPU core, so that the optimal number of sequences per file depends on how many CPU cores you have and the total number of reads as well. 

<br>

## Prediction

The shell script below takes as input paired-end reads, though both paired-end and single-end modes are supported by DeepMicrobes.
We recommend running DeepMicrobes in paired-end mode, which provides more accurate predictions than single-end mode. <br>

The following steps are required to process the sequences in test sets before loading them into the model: 
* Interleave paired-end reads
* Split the large dataset to multiple small files (for acceleration)
* Convert the fastq/fasta sequences to TFRecord

<br>

<b>To convert fastq/fasta to TFRecord for prediction:</b>

```sh
tfrec_prediction_kmer.sh -f prediction_R1.fastq -r prediction_R2.fastq -t fastq -v /path/to/vocab/tokens_merged_12mers.txt -d /path/to/DeepMicrobes/scripts -o output_dir -s 4000000 -k 12
```

Arguments: <br>
`-i` Fasta file of training set <br>
`-v` Absolute path to the vocabulary file (path/to/vocab/tokens_merged_12mers.txt) <br>
`-d` Absolute path of directory containing scripts (/path/to/DeepMicrobes/scripts) <br>
`-o` (Optional) Output dictionary containing converted TFRecord (default: tfrec) <br>
`-s` (Optional) Number of sequences per file for splitting (default: 20480000) <br>
`-k` (Optional) k-mer length (default: 12)





