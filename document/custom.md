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

[Jellyfish](https://www.cbcb.umd.edu/software/jellyfish/) is a tool for fast, memory-efficient counting of <i>k</i>-mers in DNA. 

```sh
wget http://www.cbcb.umd.edu/software/jellyfish/jellyfish-1.1.11.tar.gz
tar zxvf jellyfish-1.1.11.tar.gz
mkdir jellyfish
cd jellyfish-1.1.11
./configure --prefix=Your/Path/to/jellyfish
make -j 8
make install
```

### Step 2. Count <i>k</i>-mers in a bunch of DNA sequences

The DNA sequence file, for example, could be a fasta file containing a collection of microbial genomes.

```sh
# Try various ${k} (..., 6, 7, 8, 9, 10, 11, 12, ...)
jellyfish count -m ${k} -o output_prefix --both-strands sequences.fa 
jellyfish dump -c -t output_prefix_0 -o output_prefix.out
rm output_prefix_0
cut -f 1 output_prefix.out > output_prefix.kmers
rm output_prefix.out
```

The option `--both-strands` ensures that complementary <i>k</i>-mers will be represented with the same embedding vector.


### Step 3. Add a symbol for out-of-vocabulary <i>k</i>-mers

Add a `<unk>` symbol to the vocabulary file `output_prefix.kmers`. 
The resulted file should look like:

```
<unk>
AAAAAAAAAAAA
AAAAAAAAAAAC
AAAAAAAAAAAG
AAAAAAAAAAAT
AAAAAAAAAACA
AAAAAAAAAACC
AAAAAAAAAACG
AAAAAAAAAACT
AAAAAAAAAAGA
```

The number of <i>k</i>-mers now in `output_prefix.kmers`:

```sh
wc -l output_prefix.kmers  # vocab_size - 1
```

The `vocab_size` should be the number of k-mers in the vocabulary file plus one, because the 0th position is reserved to represent "no sequence" for variable-length sequence datasets.

