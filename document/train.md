# How to train the DNN model of DeepMicrobes

This tutorial shows how to train the DNN model of DeeMicrobes from scratch. 

<br>

## Obtain a training set

The training set can be composed of any sequences as long as you have a ground truth category label for each sequence. To train a species classifier for metagenome utilizing a collection of microbial genomes, you would need to first simulate sequencing reads from these genomes. <br>


<b>For example, to prepare the training set for the gut model from the DeepMicrobes paper (under preparation):</b> 
* Download the genomes in the complete bacterial repertoire of the human gut microbiota from this [FTP site](ftp://ftp.ebi.ac.uk/pub/databases/metagenomics/umgs_analyses). <br>
* Assign a category label for each species. <br>
* Read simulation with [ART simulator](https://academic.oup.com/bioinformatics/article/28/4/593/213322) for each genome. <br>
* Trim reads to variable lengths with the custom script `random_trim.py`. <br>
* Shuffle all the reads and convert them to TFRecord. <br>

See below for details. `random_trim.py` and `fna_label.py` can be found in [scripts](https://github.com/MicrobeLab/DeepMicrobes/blob/master/scripts).


### Label assignment

Each category should be given a ground true label which is an integer between `0` and `num_classes-1`. <br>
<b>E.g.</b>, Suppose we have 100 categories, we should assign a non-redundant integer label between 0-99 to each category. 

Please provide a label file for `fna_label.py`. The script add a label prefix for each sequence in a fasta genome file. These labels will be carried to sequence identifiers of simulated reads using ART simulator. 

The label file is a tab-delimited file which looks like:

```
genome_00.fna	0
genome_01.fna	1
genome_02.fna	2
genome_03.fna	3
genome_04.fna	4
...
genome_99.fna	99
```

The script `fna_label.py` output all the labeled fasta genome files in an user-specified dictionary. 

```sh
python fna_label.py -m /path/to/label_file.txt -o output_dir
```
Arguments:
* `-m` Tabular file mapping from names of the genome files (can be full path) to integer labels <br>
* `-o` Output dictionary

The labeled genomes we used to train the species and genus model of DeepMicrobes are available [here](https://mail2sysueducn-my.sharepoint.com/:f:/g/personal/liangqx7_mail2_sysu_edu_cn/EjQtlY1EmuZOtrUsbPCy4rQBo5rHmprL-WzvHbqzNAWVlA?e=zILdlI).


### Read simulation

We recommend generating equal proportion of reads for each category. Next-generation sequencing read simulators generally produce fixed-length reads. 

To trim the simulated reads to variable lengths:

```sh
python random_trim.py -i input_fastq -o output_fasta -f fastq -l 150 -min 0 -max 75
```
Arguments:  
* `-i` input fastq/fasta sequences (fixed-length) <br>
* `-o` output fasta sequences (variable-length) <br>
* `-f` input file type (fastq/fasta) <br>
* `-l` length of the input sequences <br>
* `-min` minimum number of trimmed bases <br>
* `-max` maximum number of trimmed bases <br>

The example command line above trims the 150bp reads from 3'end to 75-150bp. 


### TFRecord conversion

Please refer to the [TFRecord tutorial](https://github.com/MicrobeLab/DeepMicrobes/blob/master/document/tfrecord.md).

<br>

## Train a deep neural network

To train a DNN model for DeepMicrobes:

```sh
python /path/to/DeepMicrobes.py --input_tfrec=train.tfrec --model_name=attention --model_dir=/path/to/weights
```
Arguments:
* `input_tfrec` TFRecord containing sequences and their labels <br>
* `model_name` Model architecture (must be specified) <br>	
* `model_dir` Dictionary in which trained weights are saved <br>
* `batch_size` Number of sequences in one batch [32] <br>
* `num_classes` Number of classes [2505] <br>
* `kmer` K-mer length [12] <br>
* `keep_prob` Keep probability for dropout [1.0] <br>
* `vocab_size` Number of k-mers in the vocabulary file plus one [8390658] <br>
* `cpus` Number of parallel calls for input preparation [8] <br>
* `train_epochs` Number of epochs used to train [1] <br>
* `lr_decay` Learning rate decay [0.05] <br>
* `lr` Learning rate [0.001] <br>


To get a full list of training options for `DeepMicrobes.py`:

```sh
python /path/to/DeepMicrobes.py --helpfull
```


<b>Note</b>: 
* Recommended batch size for training on thousands of species is 2048 or 4096. Try a lower value when training on fewer classes. 
* `vocab_size` should match `kmer`. See the table below for `vocab_size` of the [provided vocabulary files](https://github.com/MicrobeLab/DeepMicrobes-data/tree/master/vocabulary).


| vocabulary filename | vocab_size |
| :-: | :-: |
| tokens_merged_12mers.txt | 8390658 |
| tokens_merged_11mers.txt | 2097154 |
| tokens_merged_10mers.txt | 524802 |
| tokens_merged_9mers.txt | 131074 |
| tokens_merged_8mers.txt | 32898 |

