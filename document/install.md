# How to install DeepMicrobes

A step-by-step tutorial on installation.

Note: We are working to making DeepMicrobes available on Bioconda, so that this tutorial may be frequently updated.

## 1. Clone this repository

```sh
git clone https://github.com/MicrobeLab/DeepMicrobes.git
```

<br>

## 2. Create a conda environment for DeepMicrobes

(Optional) Please install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html) first.

Note: We build and test DeepMicrobes on TensorFlow 1.9.0 and the compatibility to other versions is still being tested. 

```sh
conda env create -f DeepMicrobes/install.yml

# activate it
source activate DeepMicrobes
```

<br>

## 3. Install other dependencies

(Optional) Install `seq-shuf` (only for shuffling sequences in a training set) <br>
`seq-shuf` is available at https://github.com/thackl/seq-scripts <br>
To facilitate the installation, we'd included the script in `bin`:

```sh
export PATH=/path/to/DeepMicrobes/bin:$PATH
```


(Optional) Install `GNU Parallel` (for acceleration of TFRecord conversion) <br>
The `parallel` is also included in `bin`. Alternatively, you could install it using the command:

```sh
(wget -O - pi.dk/3 || curl pi.dk/3/) | bash
```

<br>

## 4. Download <i>k</i>-mer vocabulary files

A vocabulary file of <i>k</i>-mers is required for TFRecord conversion. To download the 12-mer vocabulary:

```sh
wget https://github.com/MicrobeLab/DeepMicrobes-data/raw/master/vocabulary/tokens_merged_12mers.txt.gz
gunzip tokens_merged_12mers.txt.gz
```

Although the vocabularies of other <i>k</i>-mers are not used in DeepMicrobes (except for the <i>k</i>-mer variant models), they could be useful when training a custom model.

```sh
wget https://github.com/MicrobeLab/DeepMicrobes-data/raw/master/vocabulary/tokens_merged_11mers.txt.gz
wget https://github.com/MicrobeLab/DeepMicrobes-data/raw/master/vocabulary/tokens_merged_10mers.txt.gz
wget https://github.com/MicrobeLab/DeepMicrobes-data/raw/master/vocabulary/tokens_merged_9mers.txt.gz
wget https://github.com/MicrobeLab/DeepMicrobes-data/raw/master/vocabulary/tokens_merged_8mers.txt.gz

gunzip tokens_merged_11mers.txt.gz
gunzip tokens_merged_10mers.txt.gz
gunzip tokens_merged_9mers.txt.gz
gunzip tokens_merged_8mers.txt.gz
```

The vocabulary file can be stored in any dictionary (hereafter referred to as `/path/to/vocab/`). 

<br>

## 5. Add scripts to path

The `pipelines` dictionary contains wrapper shell scripts for TFRecord conversion, model training, and classification. 

```sh
export PATH=/path/to/DeepMicrobes/pipelines:$PATH
export PATH=/path/to/DeepMicrobes/scripts:$PATH
export PATH=/path/to/DeepMicrobes:$PATH
```



