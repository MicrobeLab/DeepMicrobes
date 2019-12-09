#!/bin/bash

usage()
{
cat << EOF
usage: $0 options

This script makes predictions using the model of Embed + CNN. 

OPTIONS: 
   -i      TFRecord (k-mer) input containing interleaved paired-end reads
   -m      Dictionary containing model weights
   -o      Output prefix
   -b      (Optional) Batch size (a multiple of 4) (default: 8192)
   -p      (Optional) Number of parallel calls for input preparation (default: 8)

EXAMPLE:
./predict_embed_cnn.sh -i sample.tfrec -b 8192 -p 8 -m model_dir -o prefix 
EOF
}

input=
model_dir=
output_prefix=
batch_size=
cpu=


while getopts “i:m:o:b:p:” OPTION
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
         b)
             batch_size=${OPTARG}
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


if [[ -z ${input} ]] || [[ -z ${model_dir} ]] || [[ -z ${output_prefix} ]]
then
	echo "ERROR : Please supply required arguments"
	usage
	exit 1
fi

if [ -z ${batch_size} ]; then batch_size=8192; fi
if [ -z ${cpu} ]; then cpu=8; fi

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


if [[ ! -x "$(command -v DeepMicrobes.py)" ]] 
then
	echo "ERROR : Please add /path/to/DeepMicrobes dictionary to path"
	exit 1
fi


echo "Prediction started ..."

DeepMicrobes.py \
	--batch_size=${batch_size} --num_classes=2505 \
	--model_name=embed_cnn --encode_method=kmer \
	--model_dir=${model_dir} \
	--input_tfrec=${input} \
	--vocab_size=8390658 --cpus=${cpu} \
	--translate=False \
	--pred_out=${output_prefix} \
	--running_mode=predict_paired_class 

paste ${output_prefix}.category_paired.txt ${output_prefix}.prob_paired.txt > ${output_prefix}.result.txt
rm ${output_prefix}.category_paired.txt ${output_prefix}.prob_paired.txt

echo "Result: ${output_prefix}.result.txt"
