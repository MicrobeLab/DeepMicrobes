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

Arguments: 
`-i` Fasta file of training set
`-v` Absolute path to the vocabulary file (path/to/vocab/tokens_merged_12mers.txt)
`-d` Absolute path of directory containing scripts (/path/to/DeepMicrobes/scripts)
`-o` (Optional) Output dictionary containing converted TFRecord (default: tfrec)
`-s` (Optional) Number of sequences per file for splitting (default: 20480000)
`-k` (Optional) k-mer length (default: 12)


The converted TFRecord will be stored in `output_dir/train.tfrec`. 


<br>

## Prediction

The following steps are required to process the sequences in test sets before loading them into the model:
* 