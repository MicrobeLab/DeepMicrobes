# How to generate taxonomic profiles

In this tutorial we show how to summarize [read-level predictions](https://github.com/MicrobeLab/DeepMicrobes/blob/master/document/prediction.md) into a read-count profile.

The wrapper script `report_profile.sh` can be found in [pipelines](https://github.com/MicrobeLab/DeepMicrobes/tree/master/pipelines).

```sh
report_profile.sh -i predict.result.txt -o summarize.profile.txt -t 50 -l /path/to/DeepMicrobes/data/name2label.txt 
```
Arguments: <br>
* `-i` Input prediction result
* `-o` Output report
* `-t` (Optional) Threshold for confidence score in percentage % (default: 50)
* `-l` Tab-delimited file mapping from species/genus name to category label

`name2label_species.txt` and `name2label_genus.txt` are available in [data](https://github.com/MicrobeLab/DeepMicrobes/tree/master/data).

Predictions below confidence threshold are ignored. The summarized report is a tabular file showing read count for each species/genus.