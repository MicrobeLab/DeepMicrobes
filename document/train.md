# How to train the DNN model of DeepMicrobes

This tutorial shows how to train the DNN model of DeeMicrobes from scratch. 

## Obtain a training set

Theoretically, the training set can be composed of any sequences, as long as you have a ground truth category label for each sequence.

To train a species classifier for metagenome utilizing a collection of microbial genomes, you would need to first simulate sequencing reads from these genomes. <br>
<b>For example, to prepare the training set for the gut model from the DeepMicrobes paper (under preparation):</b> <br>
* 1. Download the genomes in the complete bacterial repertoire of the human gut microbiota from this [FTP site](ftp://ftp.ebi.ac.uk/pub/databases/metagenomics/umgs_analyses). <br>
* 2. Assign a category label for each species. <br>
* 3. Read simulation with [ART](https://academic.oup.com/bioinformatics/article/28/4/593/213322) for each genome. <br>
* 4. Trim reads to variable lengths with the custom script `random_trim.py`. <br>
* 5. Shuffle all the reads and convert them to TFRecord. <br>

See below for details.

### Label assignment

Each species should be assigned a non-redundant integer between `0` and `total number of species`. 
Suppose we 100 categories, we should assign a non-redundant integer label between 0-99 to each category.

### Read simulation

### TFRecord conversion


<br>

## Train a deep neural network


