## Converting sequences to TFRecord

### One-hot encoding

    seq2tfrec_onehot.py --input_seq=input.fasta \
                        --output_tfrec=output.tfrec \
                        --label=/path/to/label2taxid.txt \
                        --is_train=True \
                        --seq_type=fasta
  

### K-mer embedding

    export PYTHONPATH=$PYTHONPATH:/path/to/DeepMicrobes
  
    seq2tfrec_kmer.py --input_seq=input.fasta \
                      --output_tfrec=output.tfrec \
                      --label=/path/to/label2taxid.txt \
                      --is_train=True \
                      --seq_type=fasta \
                      --kmer=12 \
                      --vocab=/path/to/token_12mer


The vocabulary file of merged 12-mers can be downloaded [here](https://mail2sysueducn-my.sharepoint.com/:f:/g/personal/liangqx7_mail2_sysu_edu_cn/EoMaqt1sNbZHl9kFj84WvnsBT4dPFN_Yddkm0bo87Fms8g?e=KLgguV). 


## Before test set conversion

Taking the average of two softmax probabilities of reverse complement sequences could improve performance. For paired-end data we suggest users take the average of four softmax probabilities. The averaging process is automatically carried out by DeepMicrobes. To this end, an interleaved fasta (or fastq) file should be provided to the scripts above. Interleaved data could be generated using [seqtk](https://github.com/lh3/seqtk/releases).

### Single-end data

    seqtk seq -r sequences.fa > sequences_reverse_complement.fa
    seqtk mergepe sequences.fa sequences_reverse_complement.fa > sequences_interleaved.fa
    
### Paired-end data

    seqtk seq -r sequences_R1.fa > sequences_rc_R1.fa
    seqtk seq -r sequences_R2.fa > sequences_rc_R2.fa
    seqtk mergepe sequences_R1.fa sequences_rc_R1.fa > sequences_interleaved_R1.fa
    seqtk mergepe sequences_R2.fa sequences_rc_R2.fa > sequences_interleaved_R2.fa
    seqtk mergepe sequences_interleaved_R1.fa sequences_interleaved_R2.fa > sequences_interleaved_merged.fa
