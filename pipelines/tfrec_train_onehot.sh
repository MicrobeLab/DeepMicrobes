#!/bin/bash

usage()
{
cat << EOF
usage: $0 options

This script takes as input fasta sequences for training and returns converted TFRecord (one-hot).  

OPTIONS: 
   -i      Fasta file of training set
   -d      Absolute path of directory containing scripts (/path/to/DeepMicrobes/scripts)
   -o      Output name of converted TFRecord
   -s      (Optional) Number of sequences per file for splitting (default: 20480000)

EXAMPLE:
./tfrec_train_onehot.sh -i train.fa -d DeepMicrobes/scripts -o train.tfrec -s 20480000
EOF
}

input_fasta=
script_dir=
output_tfrec=
split_seq=


while getopts “i:d:o:s:” OPTION
do
     case ${OPTION} in
         i)
             input_fasta=${OPTARG}
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
         ?)
             usage
             exit
             ;;
     esac
done


if [[ -z ${input_fasta} ]] || [[ -z ${script_dir} ]] || [[ -z ${output_tfrec} ]]
then
     echo "ERROR : Please supply required arguments"
     usage
     exit 1
fi

if [ -z ${split_seq} ]; then split_seq=20480000; fi

line=$( expr ${split_seq} \* 2 )


if [ -x "$(command -v parallel)" ];
then
	echo "parallel successfully detected..."
else
	echo "ERROR : parallel not detected"
	exit 1
fi

if [ -x "$(command -v seq-shuf)" ];
then
	echo "seq-shuf successfully detected..."
else
	echo "ERROR : seq-shuf not detected"
	exit 1
fi


if [ ! -e ${input_fasta} ]; then
    echo "ERROR : Missing fasta reads for training!"
	usage
    exit 1
fi


if [ ! -d ${script_dir} ];then
    echo "ERROR : Missing the dictionary containing seq2tfrec_onehot.py!"
    usage
    exit 1
fi

if [ ! -e ${script_dir}/seq2tfrec_onehot.py ]; then
    echo "ERROR : Missing seq2tfrec_onehot.py!"
	usage
	exit 1
fi

echo "Starting converting ${input_fasta} to TFRecord (mode=training), output will be saved in ${output_tfrec}"
echo "Parameters: split_size=${split_seq}"


echo "======================================"
echo "1. Shuffling sequences for training..."
if [ -d tmp_tfrec_${input_fasta} ]; then rm -rf tmp_tfrec_${input_fasta}; fi
mkdir tmp_tfrec_${input_fasta}
cat ${input_fasta} | seq-shuf > tmp_tfrec_${input_fasta}/shuffled_${input_fasta}
echo " "

echo "======================================"
echo "2. Splitting input to ${split_seq} sequences per file..."
cd tmp_tfrec_${input_fasta}
split -d -l ${line} shuffled_${input_fasta} subset_${input_fasta}_
rm shuffled_${input_fasta}
echo " "

echo "======================================"
echo "3. Converting to TFRecord..."
ls subset* > tmp_fa_list

cat tmp_fa_list | parallel python ${script_dir}/seq2tfrec_onehot.py --input_seq={} --output_tfrec={}.onehot.tfrec --is_train=True --seq_type=fasta

for fa in $(cat tmp_fa_list)
do
rm $fa
done

rm tmp_fa_list

cat subset*.tfrec > ../${output_tfrec}

rm subset*.tfrec
cd ..
rmdir tmp_tfrec_${input_fasta}

echo "Finished."


