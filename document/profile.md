# How to generate taxonomic profiles

In this tutorial we show how to summarize [read-level predictions](https://github.com/MicrobeLab/DeepMicrobes/blob/master/document/prediction.md) into a read-count profile.

The wrapper script `report_profile.sh` can be found in [pipelines](https://github.com/MicrobeLab/DeepMicrobes/tree/master/pipelines).

```sh
report_profile.sh -i predict.result.txt -o summarize.profile.txt -t 0.50 -m /path/to/DeepMicrobes/data/name2label.txt
```
Arguments: <br>
* `-i`: Input prediction result
* `-o`: Output report
* `-t`: (Optional) Threshold for confidence score (default: 0.50)
* `-m`: Tab-delimited file mapping from species/genus name to category label

`name2label_species.txt` and `name2label_genus.txt` are available in [data](https://github.com/MicrobeLab/DeepMicrobes/tree/master/data).

