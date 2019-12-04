#!/bin/bash

usage()
{
cat << EOF
usage: $0 options

This script summarizes read-level predictions into a profile. 

OPTIONS: 
   -i      Input prediction result
   -o      Output report
   -t      (Optional) Threshold for confidence score (default: 0.50)
   -l      Tab-delimited file mapping from species/genus name to category label

EXAMPLE:
./report_profile.sh -i predict.result.txt -o summarize.profile.txt -t 0.50 -l /path/to/DeepMicrobes/data/name2label.txt
EOF
}
