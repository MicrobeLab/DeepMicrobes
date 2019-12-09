#!/bin/bash

usage()
{
cat << EOF
usage: $0 options

This script takes as input fastq/fasta sequences for prediction and returns converted TFRecord (one-hot).  

OPTIONS: 
   -f      Fastq/fasta file of forward reads
   -r      Fastq/fasta file of reverse reads
   -o      Output name prefix
   -s      (Optional) Number of sequences per file for splitting (default: 4000000)
   -t      (Optional) Sequence type fastq/fasta (default: fastq)

EXAMPLE:
./tfrec_predict_onehot.sh -f sample_R1.fastq -r sample_R2.fastq -t fastq -o sample_name -s 4000000 
EOF
}

forward=
reverse=
output_name=
split_seq=
seq_type=


while getopts “f:r:o:s:t:” OPTION
do
     case ${OPTION} in
         f)
             forward=${OPTARG}
             ;;
         r)
             reverse=${OPTARG}
             ;;
         o)
             output_name=${OPTARG}
             ;;
         s)
             split_seq=${OPTARG}
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


if [[ -z ${forward} ]] || [[ -z ${reverse} ]] || [[ -z ${output_name} ]]
then
	echo "ERROR : Please supply required arguments"
	usage
	exit 1
fi

if [ -z ${split_seq} ]; then split_seq=4000000; fi
if [ -z ${seq_type} ]; then seq_type=fastq; fi

if [ "$seq_type" = fastq ] 
then 
	line=$( expr ${split_seq} \* 4 )
elif [ "$seq_type" = fasta ] 
then
	line=$( expr ${split_seq} \* 2 )
else
	echo "ERROR : Sequence type must be 'fasta' or 'fastq'"
	usage
	exit 1
fi


fragment_num=$(( ${split_seq} % 4 ))

if [ ${fragment_num} != 0 ]
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

if [ -x "$(command -v seqtk)" ];
then
	echo "seqtk successfully detected..."
else
	echo "ERROR : seqtk not detected"
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


if [ ! -x "$(command -v seq2tfrec_onehot.py)" ]; then
    echo "ERROR : Please add /path/to/DeepMicrobes/scripts dictionary to path"
	exit 1
fi


echo "Starting converting ${forward} and ${reverse} to TFRecord (mode=prediction), output will be saved in ${output_name}.tfrec"
echo "Parameters: split_size=${split_seq}, sequence_type=${seq_type}"

echo "======================================"
echo "1. Interleaving R1 and R2..."

seqtk seq -r ${forward} > ${forward}.rc
seqtk seq -r ${reverse} > ${reverse}.rc

seqtk mergepe ${forward} ${reverse} > tmp_fs_${output_name}.${seq_type}
seqtk mergepe ${forward}.rc ${reverse}.rc > tmp_rs_${output_name}.${seq_type}
seqtk mergepe tmp_fs_${output_name}.${seq_type} tmp_rs_${output_name}.${seq_type} > ${output_name}.merged.${seq_type} 

rm ${forward}.rc ${reverse}.rc
rm tmp_fs_${output_name}.${seq_type} tmp_rs_${output_name}.${seq_type}
echo " "

echo "======================================"
echo "2. Splitting the merged file to ${split_seq} sequences per file..."

if [ -d tmp_tfrec_${output_name} ]; then rm -rf tmp_tfrec_${output_name}; fi
mkdir tmp_tfrec_${output_name}
cd tmp_tfrec_${output_name}

split -d -l ${line} ../${output_name}.merged.${seq_type} subset_${output_name}_
rm ../${output_name}.merged.${seq_type}
echo " "

echo "======================================"
echo "3. Converting to TFRecord..."
ls subset* > tmp_${seq_type}_list

cat tmp_${seq_type}_list | parallel seq2tfrec_onehot.py --input_seq={} --output_tfrec={}.onehot.tfrec --is_train=False --seq_type=${seq_type}

for seq in $(cat tmp_${seq_type}_list)
do
rm $seq
done

rm tmp_${seq_type}_list

cat subset*.tfrec > ../${output_name}.tfrec

rm subset*.tfrec
cd ..
rmdir tmp_tfrec_${output_name}

echo "Finished."


	
