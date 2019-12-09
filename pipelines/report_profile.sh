#!/bin/bash

usage()
{
cat << EOF
usage: $0 options

This script summarizes read-level predictions into a profile. 

OPTIONS: 
   -i      Input prediction result
   -o      Output report
   -t      (Optional) Threshold for confidence score in percentage % (default: 50)
   -l      Tab-delimited file mapping from species/genus name to category label

EXAMPLE:
./report_profile.sh -i predict.result.txt -o summarize.profile.txt -t 50 -l /path/to/DeepMicrobes/data/name2label.txt 
EOF
}


input=
output=
threshold=
label=


while getopts “i:o:t:l:” OPTION
do
     case ${OPTION} in
         i)
             input=${OPTARG}
             ;;
         o)
             output=${OPTARG}
             ;;
         t)
             threshold=${OPTARG}
             ;;
         l)
             label=${OPTARG}
             ;;
         ?)
             usage
             exit
             ;;
     esac
done


if [[ -z ${input} ]] || [[ -z ${output} ]] || [[ -z ${label} ]]
then
	echo "ERROR : Please supply required arguments"
	usage
	exit 1
fi

if [ -z ${threshold} ]; then threshold=50; fi

if [[ ${threshold} -gt 100 ]] || [[ ${threshold} -lt 0 ]]
then
	echo "ERROR : Confidence threshold (%) should between 0 and 100"
	usage
	exit 1
fi

if [[ 1 -eq "$(echo "${threshold} < 1" | bc)" ]] && [[ 1 -eq "$(echo "${threshold} > 0" | bc)" ]]
then  
    echo "WARNING : Confidence threshold (%) should be percentage between 0 and 100"
    usage
fi


if [ ! -e ${input} ]; then
    echo "ERROR : Input prediction result not found"
	usage
    exit 1
fi

if [ ! -e ${label} ]; then
    echo "ERROR : Label mapping file not found"
	usage
    exit 1
fi


if [ ! -x "$(command -v read_counter.py)" ]; then
    echo "ERROR: Please add /path/to/DeepMicrobes/scripts dictionary to path"
	exit 1
fi


echo "Filtering predictions using threshold ${threshold} (%) ..."

awk -v var="$threshold" '$2>=var' ${input} > ${input}.filtered.txt

echo "Summarizing predictions ..."

read_counter.py -i ${input}.filtered.txt -o ${output} -l ${label}

rm ${input}.filtered.txt

echo "Finished."
