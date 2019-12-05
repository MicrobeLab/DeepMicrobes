# Getting start with DeepMicrobes

In this tutorial we provide an example how to perform taxonomic classification on a metagenome dataset with DeepMicrobes.

We will analyze a real gut metagenome sample using the pre-trained weights of the species model.

Please replace all the pseudo paths `/path/to/` below with the actual path. 

## Step 1. Install DeepMicrobes

Please follow the step-by-step tutorial [here](https://github.com/MicrobeLab/DeepMicrobes/blob/master/document/install.md). 
Be sure to download the best performing species model of DeepMicrobes.

```sh
# species model
wget -O "weights_species.tar.gz" https://onedrive.gimhoy.com/sharepoint/aHR0cHM6Ly9tYWlsMnN5c3VlZHVjbi1teS5zaGFyZXBvaW50LmNvbS86dTovZy9wZXJzb25hbC9saWFuZ3F4N19tYWlsMl9zeXN1X2VkdV9jbi9FU0EtWnZwdVlqcEZqTHlkb2U2Tzl2OEJLOW5PbnFrdkdvOWpuaW56VGE5V0tnP2U9dGo2b3Vo.weights_species.tar.gz
tar -xzvf weights_species.tar.gz
```

Alternatively, you could manually download the weights [here](https://mail2sysueducn-my.sharepoint.com/:u:/g/personal/liangqx7_mail2_sysu_edu_cn/ESA-ZvpuYjpFjLydoe6O9v8BK9nOnqkvGo9jninzTa9WKg?e=3rDFBd).

## Step 2. Download the example data

```sh
wget https://github.com/MicrobeLab/DeepMicrobes-data/raw/master/gut_metagenome/SRR5935743_clean_1.fastq.gz
wget https://github.com/MicrobeLab/DeepMicrobes-data/raw/master/gut_metagenome/SRR5935743_clean_2.fastq.gz

gunzip SRR5935743_clean_1.fastq.gz
gunzip SRR5935743_clean_2.fastq.gz
```

This is a quality controlled gut metagenome from the IBD (inflammatory bowel disease) study of iHMP. We chose this small dataset for illustration purpose. 

## Step 3. Convert the fastq files to TFRecord

```sh
tfrec_predict_kmer.sh \
	-f /path/to/SRR5935743_clean_1.fastq \
	-r /path/to/SRR5935743_clean_2.fastq \
	-t fastq \
	-v /path/to/vocab/tokens_merged_12mers.txt \
	-d /path/to/DeepMicrobes/scripts \
	-o SRR5935743 \
	-s 4000000 \
	-k 12
```

In the current dictionary you will find `SRR5935743.tfrec`.

## Step 4. Make prediction

```sh
predict_DeepMicrobes.sh \
	-i SRR5935743.tfrec \
	-b 8192 \
	-l species \
	-p 8 \
	-m /path/to/weights_species \
	-o SRR5935743 \
	-d /path/to/DeepMicrobes
```

Try a smaller batch size (-b) if you encounter out-of-memory error. Be sure to set the value to a multiple of 4.

The predicted results will be saved in `SRR5935743.result.txt` in the current dictionary.

## Step 5. Generate profile

```sh
report_profile.sh \
	-i SRR5935743.result.txt \
	-o SRR5935743.profile.txt \
	-t 50 \
	-l /path/to/DeepMicrobes/data/name2label_species.txt \
	-d /path/to/DeepMicrobes/scripts
```

The output `SRR5935743.profile.txt` is a tabular file showing the number of reads assigned to each species. 




