#!/bin/bash

usage()
{
cat << EOF
usage: $0 options

This script takes as input fastq/fasta sequences for prediction and returns converted TFRecord.  

OPTIONS: 
   -f      Fastq/fasta file of forward reads
   -r      Fastq/fasta file of reverse reads
   -v      Absolute path to the vocabulary file (path/to/tokens_merged_12mers.txt)
   -d      Absolute path of directory containing scripts (/path/to/DeepMicrobes/scripts)
   -o      Output name of converted TFRecord
   -s      (Optional) Number of sequences per file for splitting (default: 4000000)
   -k      (Optional) k-mer length (default: 12)
   -t      (Optional) Sequence type fastq/fasta (default: fastq)

EXAMPLE:
./tfrec_predict_kmer.sh -f sample_R1.fastq -r sample_R2.fastq -t fastq -v /path/to/vocab/tokens_merged_12mers.txt -d /path/to/DeepMicrobes/scripts -o sample.tfrec -s 4000000 -k 12
EOF
}

forward=
reverse=
vocab=
script_dir=
output_tfrec=
split_seq=
kmer=
seq_type=


while getopts “f:r:v:d:o:s:k:t:” OPTION
do
     case ${OPTION} in
         f)
             forward=${OPTARG}
             ;;
         r)
             reverse=${OPTARG}
             ;;
         v)
             vocab=${OPTARG}
             ;;
         d)
             script_dir=${OPTARG}
             ;;
         o)
             output_tfrec=${OPTARG}
             ;;
         s)
             split_seq=${OPTARG}
             ;; 
         k)
             kmer=${OPTARG}
             ;; 
         t)
             seq_type=${OPTARG}
             ;;   
         ?)
             usage
             exit
             ;;
     esac
done


if [[ -z ${forward} ]] || [[ -z ${reverse} ]] || [[ -z ${vocab} ]] || [[ -z ${script_dir} ]] || [[ -z ${output_tfrec} ]]
then
	echo "ERROR : Please supply required arguments"
	usage
	exit 1
fi

if [ -z ${split_seq} ]; then split_seq=4000000; fi
if [ -z ${kmer} ]; then kmer=12; fi
if [ -z ${seq_type} ]; then seq_type=fastq; fi

if [ "$seq_type" = fastq] 
then 
	line=$( expr ${split_seq} \* 4 )
elif [ "$seq_type" = fasta] 
then
	line=$( expr ${split_seq} \* 2 )
else
	echo "ERROR : Sequence type must be 'fasta' or 'fastq'"
	usage
	exit 1
fi


if [ $(( ${split_seq} % 4 != 0)) 
then
	echo "ERROR: The number of sequences per file must a multiple of 4 for paired-end data"
	exit 1
fi


if [ -x "$(command -v parallel)" ];
then
	echo "parallel successfully detected..."
else
	echo "ERROR : parallel not detected"
	exit 1
fi


if [ ! -e ${forward} ]; then
    echo "ERROR : Missing forward reads (R1)!"
	usage
    exit 1
fi

if [ ! -e ${reverse} ]; then
    echo "ERROR : Missing reverse reads (R2)!"
	usage
    exit 1
fi

if [ ! -e ${vocab} ]; then
    echo "ERROR : Missing the vocabulary file!"
	usage
	exit 1
fi

if [ ! -d ${script_dir} ];then
    echo "ERROR : Missing the dictionary containing seq2tfrec_kmer.py!"
    usage
    exit 1
fi

if [ ! -e ${script_dir}/seq2tfrec_kmer.py ]; then
    echo "ERROR : Missing seq2tfrec_kmer.py!"
	usage
	exit 1
fi


echo "Starting converting ${forward} and ${reverse} to TFRecord (mode=prediction), output will be saved in ${output_tfrec}"
echo "Parameters: kmer=${kmer}, vocab_file=${vocab}, split_size=${split_seq}, sequence_type=${seq_type}"

echo "======================================"
echo "1. Interleaving R1 and R2..."




