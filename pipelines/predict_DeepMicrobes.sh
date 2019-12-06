#!/bin/bash

usage()
{
cat << EOF
usage: $0 options

This script takes as input a TFRecord format metagenome and performs taxonomic classification for each pair of reads. 

OPTIONS: 
   -i      TFRecord input containing interleaved paired-end reads
   -m      Dictionary containing model weights (should match the taxonomic level)
   -o      Output prefix
   -d      Dictionary containing the main script DeepMicrobes.py
   -b      (Optional) Batch size (a multiple of 4) (default: 8192)
   -l      (Optional) Taxonomic level, species/genus (should match the weights) (default: species)
   -p      (Optional) Number of parallel calls for input preparation (default: 8)

EXAMPLE:
./predict_DeepMicrobes.sh -i sample.tfrec -b 8192 -l species -p 8 -m model_dir -o prefix -d /path/to/DeepMicrobes
EOF
}


input=
model_dir=
output_prefix=
main_dir=
batch_size=
level=
cpu=

while getopts “i:m:o:d:b:l:p:” OPTION
do
     case ${OPTION} in
         i)
             input=${OPTARG}
             ;;
         m)
             model_dir=${OPTARG}
             ;;
         o)
             output_prefix=${OPTARG}
             ;;
         d)
             main_dir=${OPTARG}
             ;;
         b)
             batch_size=${OPTARG}
             ;;
         l)
             level=${OPTARG}
             ;;
         p)
             cpu=${OPTARG}
             ;; 
         ?)
             usage
             exit
             ;;
     esac
done


if [[ -z ${input} ]] || [[ -z ${model_dir} ]] || [[ -z ${output_prefix} ]] || [[ -z ${main_dir} ]]
then
	echo "ERROR : Please supply required arguments"
	usage
	exit 1
fi

if [ -z ${batch_size} ]; then batch_size=8192; fi
if [ -z ${level} ]; then level=species; fi
if [ -z ${cpu} ]; then cpu=8; fi

if [ "$level" = species] 
then 
	num_classes=2505
elif [ "$level" = genus] 
then
	num_classes=120
else
	echo "ERROR : Taxonomic level must be 'species' or 'genus'"
	usage
	exit 1
fi

fragment_num=$(( ${batch_size} % 4 ))

if [ ${fragment_num} != 0 ]
then
	echo "ERROR: Batch size must a multiple of 4 for paired-end data"
	exit 1
fi

if [ ! -e ${input} ]; then
    echo "ERROR : Input TFRecord not found"
	usage
    exit 1
fi

if [ ! -d ${model_dir} ];then
    echo "ERROR : model_dir not found"
    usage
    exit 1
fi

if [[ ! -e ${model_dir}/checkpoint ]] || [[ ! -e ${model_dir}/graph.pbtxt ]] || [[ ! -e ${model_dir}/model.ckpt-0.data-00000-of-00001 ]] || [[ ! -e ${model_dir}/model.ckpt-0.index ]] || [[ ! -e ${model_dir}/model.ckpt-0.meta ]] 
then
    echo "ERROR : Missing all or part of the model weight files"
	usage
	exit 1
fi

if [ ! -d ${main_dir} ];then
    echo "ERROR : Dictionary containing DeepMicrobes.py not found"
    usage
    exit 1
fi

if [[ ! -e ${main_dir}/DeepMicrobes.py ]] 
then
	echo "ERROR : DeepMicrobes.py not found in ${main_dir}"
	usage
	exit 1
fi


echo "Prediction started ..."

python ${main_dir}/DeepMicrobes.py \
	--batch_size=${batch_size} --num_classes=${num_classes} \
	--model_name=attention --encode_method=kmer \
	--model_dir=${model_dir} \
	--input_tfrec=${input} \
	--vocab_size=8390658 --cpus=${cpu} \
	--translate=False \
	--pred_out=${output_prefix} \
	--running_mode=predict_paired_class 

paste ${output_prefix}.category_paired.txt ${output_prefix}.prob_paired.txt > ${output_prefix}.result.txt
rm ${output_prefix}.category_paired.txt ${output_prefix}.prob_paired.txt

echo "Prediction finished ..."
echo "Result: ${output_prefix}.result.txt"

