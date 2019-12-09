# How to install DeepMicrobes

A step-by-step tutorial on installation.

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

## 3. Download pre-trained weights

We provide the pre-trained weights for the species and genus level DeepMicrobes models, as well as the species models of other tested DNN architectures. <br>
The models were trained on the [complete bacterial repertoire of the human gut microbiota](https://www.nature.com/articles/s41586-019-0965-1).

<br>

<b>Download the weights for DeepMicrobes via the OneDrive website: </b>
* [Species model](https://mail2sysueducn-my.sharepoint.com/:u:/g/personal/liangqx7_mail2_sysu_edu_cn/ESA-ZvpuYjpFjLydoe6O9v8BK9nOnqkvGo9jninzTa9WKg?e=3rDFBd)
* [Genus model](https://mail2sysueducn-my.sharepoint.com/:u:/g/personal/liangqx7_mail2_sysu_edu_cn/EdmvxWRsEPxMvBAecrE8XD0BpH5fGBq-eTCGDqAUrJ0uLw?e=lLE7FB)

<br>

<b>Download the weights for DeepMicrobes via command lines: </b>

```sh
# species model
wget -O "weights_species.tar.gz" https://onedrive.gimhoy.com/sharepoint/aHR0cHM6Ly9tYWlsMnN5c3VlZHVjbi1teS5zaGFyZXBvaW50LmNvbS86dTovZy9wZXJzb25hbC9saWFuZ3F4N19tYWlsMl9zeXN1X2VkdV9jbi9FU0EtWnZwdVlqcEZqTHlkb2U2Tzl2OEJLOW5PbnFrdkdvOWpuaW56VGE5V0tnP2U9dGo2b3Vo.weights_species.tar.gz
tar -xzvf weights_species.tar.gz

# genus model
wget -O "weights_genus.tar.gz" https://onedrive.gimhoy.com/sharepoint/aHR0cHM6Ly9tYWlsMnN5c3VlZHVjbi1teS5zaGFyZXBvaW50LmNvbS86dTovZy9wZXJzb25hbC9saWFuZ3F4N19tYWlsMl9zeXN1X2VkdV9jbi9FZG12eFdSc0VQeE12QkFlY3JFOFhEMEJwSDVmR0JxLWVUQ0dEcUFVckowdUx3P2U9bExFN0ZC.weights_genus.tar.gz
tar -xzvf weights_genus.tar.gz
```

<br>

The weights for other tested DNNs are available here:
* [Convolutional model (ResNet-like CNN)](https://mail2sysueducn-my.sharepoint.com/:u:/g/personal/liangqx7_mail2_sysu_edu_cn/EQNhB-U1upFNtZZlzdOVLBgBtsCs-fcz00px6TERDFqOVw?e=Clk6dl)
* [Hybrid convolutional and recurrent model (CNN + LSTM)](https://mail2sysueducn-my.sharepoint.com/:u:/g/personal/liangqx7_mail2_sysu_edu_cn/EZiexqRsqABBisev9p50J94BNiAjQSRgxk1exjnNB8pR-g?e=Lw8urK)
* [Seq2species](https://mail2sysueducn-my.sharepoint.com/:u:/g/personal/liangqx7_mail2_sysu_edu_cn/EXi8l1a1ZQdOhER-j_RzJeoBydK5g_iY3tReU0sxCDF1_Q?e=3lKtjr)
* [Embedding baseline (Embed + Pool)](https://mail2sysueducn-my.sharepoint.com/:u:/g/personal/liangqx7_mail2_sysu_edu_cn/Ea4Lt-PGeQ5OlHMESsolM6MBt7aASsQbplNFxnmZrXeugg?e=WZamVV)
* [Embedding-based convolutional model (Embed + CNN)](https://mail2sysueducn-my.sharepoint.com/:u:/g/personal/liangqx7_mail2_sysu_edu_cn/Ecp123o3q05Khiv40JwlPLEBxLMsjFW6yTgQADMBuaQuVw?e=6Vi1ia)
* [Embedding-based recurrent model (Embed + LSTM)](https://mail2sysueducn-my.sharepoint.com/:u:/g/personal/liangqx7_mail2_sysu_edu_cn/EWtuF62RGO9Auc3zFXRQtjQBzh48Ku9kFuqV10IAPlP-fg?e=e6k69X)

<br>

The weights for the other <i>k</i>-mer variants of DeepMicrobes are available here:
* [8-mer](https://mail2sysueducn-my.sharepoint.com/:u:/g/personal/liangqx7_mail2_sysu_edu_cn/EfN_S0kOGzZIpnFORqL-gmEBimBN5sDcCeherfOQiPqeeQ?e=lCi1Bg)
* [9-mer](https://mail2sysueducn-my.sharepoint.com/:u:/g/personal/liangqx7_mail2_sysu_edu_cn/ERFGWt-3UvBKqOfG0tnNMMYBiVsz0ON-sQTzMB0asnCYJA?e=dHpzSm)
* [10-mer](https://mail2sysueducn-my.sharepoint.com/:u:/g/personal/liangqx7_mail2_sysu_edu_cn/EdNX8OcMjtxJj9_Qk94EXL8BM4yku1PT0Z6JPl5wgBmrdw?e=nXtSqs)
* [11-mer](https://mail2sysueducn-my.sharepoint.com/:u:/g/personal/liangqx7_mail2_sysu_edu_cn/EZZj2aa9wkVHquvhT52sXBsBvvSU5PCm-0pheeEzA4mEyg?e=8eSRzA)

<br>

The model weight files can be stored in any dictionary but files for different models should be stored in different dictionaries. 
In the following tutorials we will refer to the dictionary containing weight files (of the model you would like to use) as `model_dir`. 

<br>

## 4. Install other dependencies

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

## 5. Download <i>k</i>-mer vocabulary files

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

## 6. Add scripts to path

The `pipelines` dictionary contains wrapper shell scripts for TFRecord conversion, model training, and classification. 

```sh
export PATH=/path/to/DeepMicrobes/pipelines:$PATH
export PATH=/path/to/DeepMicrobes/scripts:$PATH
export PATH=/path/to/DeepMicrobes:$PATH
```



