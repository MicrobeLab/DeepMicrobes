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
tfrec_train_kmer.sh -i train.fa -v /path/to/vocab/tokens_merged_12mers.txt -o train.tfrec -s 20480000 -k 12
```

Arguments: <br>
`-i` Fasta file of training set <br>
`-v` Absolute path to the vocabulary file (path/to/vocab/tokens_merged_12mers.txt) <br>
`-o` Output name of converted TFRecord <br>
`-s` (Optional) Number of sequences per file for splitting (default: 20480000) <br>
`-k` (Optional) <i>k</i>-mer length (default: 12)

The converted TFRecord will be stored in `train.tfrec` (or other specified names) in the current dictionary. <br>
<br>
<b>NOTE</b>: 
* The script parses category labels from sequence IDs starting with `prefix|label` (e.g., >this_is_prefix|0).  <br>
* Suppose we have 100 categories, we should assign a non-redundant integer label between 0-99 to each category. <br>
* The label is taken as ground truth during training and not required during prediction. <br>
* Each subset files are processed with one CPU core, so that the optimal number of sequences per file depends on how many CPU cores you have and the total number of reads as well. <br>
* The vocabulary file and <i>k</i>-mer length should be matched.

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
tfrec_predict_kmer.sh -f sample_R1.fastq -r sample_R2.fastq -t fastq -v /path/to/vocab/tokens_merged_12mers.txt -o sample_name -s 4000000 -k 12
```

Arguments: <br>
`-f` Fastq/fasta file of forward reads <br>
`-r` Fastq/fasta file of reverse reads <br>
`-v` Absolute path to the vocabulary file (path/to/vocab/tokens_merged_12mers.txt) <br>
`-o` Output name prefix <br>
`-s` (Optional) Number of sequences per file for splitting (default: 4000000) <br>
`-k` (Optional) k-mer length (default: 12) <br>
`-t` (Optional) Sequence type fastq/fasta (default: fastq)

The converted TFRecord will be stored in `sample.tfrec` (or other specified names) in the current dictionary. <br>
<br>
<b>NOTE</b>: 
* Each subset files are processed with one CPU core, so that the optimal number of sequences per file depends on how many CPU cores you have and the total number of reads as well. <br>
* The vocabulary file and <i>k</i>-mer length should be matched.
* The number of sequences per file must be a multiple of 4 (complementary reads of R1 and R2).

<br>


## One-hot encoding

We also provide wrapper scripts of one-hot encoding for users who would like to play with the other tested DNNs. 

### Training set (one-hot)

```sh
tfrec_train_onehot.sh -i train.fa -o train.tfrec -s 20480000 
```

Arguments: <br>
`-i` Fasta file of training set <br>
`-o` Output name of converted TFRecord <br>
`-s` (Optional) Number of sequences per file for splitting (default: 20480000) <br>


### Test set (one-hot)

```sh
tfrec_predict_onehot.sh -f sample_R1.fastq -r sample_R2.fastq -t fastq -o sample_name -s 4000000 
```

Arguments: <br>
`-f` Fastq/fasta file of forward reads <br>
`-r` Fastq/fasta file of reverse reads <br>
`-o` Output name prefix <br>
`-s` (Optional) Number of sequences per file for splitting (default: 4000000) <br>
`-t` (Optional) Sequence type fastq/fasta (default: fastq)

