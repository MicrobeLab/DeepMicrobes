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
