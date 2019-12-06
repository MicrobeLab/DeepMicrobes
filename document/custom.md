# Suggestions on training a custom model

The deep learning architecture of DeepMicrobes can be potentially applied in biological fields beyond taxonomic classification for metagenome.

We observed that DeepMicrobes is insensitive to most of the hyperparameters (e.g., dimensions of the layers, learning rate, ...) and we've set the best performing hyperparameters as default values. 

The only hyperparameter that advanced users are required to pay attention to is `kmer`. 
As is suggested in the paper, 
researches who may want to use <i>k</i>-mer embedding in other scenarios should try different <i>k</i>-mer lengths (e.g., 6-12 bp) 
to finally find a balance between underfitting and overfitting, especially when training on only a few categories. 
For example, we noticed that 7-mer worked well for a 10-species classifier. 
Apart from the vocabulary files we provided, users could build their own <i>k</i>-mer vocabulary.

## Build a custom vocabulary

### Step 1. Install Jellyfish

[Jellyfish](https://www.cbcb.umd.edu/software/jellyfish/) is a tool for fast, memory-efficient counting of k-mers in DNA. 

```sh
wget http://www.cbcb.umd.edu/software/jellyfish/jellyfish-1.1.11.tar.gz
tar zxvf jellyfish-1.1.11.tar.gz
mkdir jellyfish
cd jellyfish-1.1.11
./configure --prefix=Your/Path/to/jellyfish
make -j 8
make install
```

### Step 2. 