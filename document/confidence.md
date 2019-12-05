# How to choose the confidence threshold

To give some guidance toward selecting an appropriate confidence threshold, we show here the results of different thresholds on the [benchmark datasets](https://github.com/MicrobeLab/DeepMicrobes-data/tree/master/benchmark_datasets) from the DeepMicrobes paper (under preparation).

<b>Note</b>: The default threshold for both the species and genus model of DeepMicrobes is 50%, which ensures >0.95 read-level specificity. 

## Species model of DeepMicrobes

The results of the species model were measured on simulated variable-length reads from gut-derived MAGs.

| Confidence (%) | Specificity | Sensitivity |
| - | - | - |
| 0 | 0.740 | 0.740 |
| 5 | 0.740 | 0.740 |
| 10 | 0.746 | 0.739 |
| 15 | 0.764 | 0.736 |
| 20 | 0.795 | 0.727 |
| 25 | 0.852 | 0.701 |
| 30 | 0.877 | 0.657 |
| 35 | 0.894 | 0.619 |
| 40 | 0.912 | 0.577 |
| 45 | 0.931 | 0.528 |
| 50 | 0.955 | 0.451 |
| 55 | 0.965 | 0.381 |
| 60 | 0.973 | 0.332 |
| 65 | 0.978 | 0.285 |
| 70 | 0.983 | 0.237 |
| 75 | 0.986 | 0.175 |
| 80 | 0.988 | 0.133 |
| 85 | 0.990 | 0.104 |
| 90 | 0.991 | 0.077 |
| 95 | 0.993 | 0.049 |
| 100 | 0.994 | 0.001 |


## Genus model of DeepMicrobes

The results of the genus model were averaged over the ten mock communities.

| Confidence (%) | Specificity | Sensitivity |
| - | - | - |
| 0 | 0.899 | 0.899 |
| 5 | 0.899 | 0.899 |
| 10 | 0.899 | 0.899 |
| 15 | 0.899 | 0.899 |
| 20 | 0.900 | 0.899 |
| 25 | 0.902 | 0.899 |
| 30 | 0.907 | 0.898 |
| 35 | 0.914 | 0.895 |
| 40 | 0.924 | 0.891 |
| 45 | 0.938 | 0.885 |
| 50 | 0.969 | 0.866 |
| 55 | 0.980 | 0.816 |
| 60 | 0.984 | 0.793 |
| 65 | 0.987 | 0.774 |
| 70 | 0.989 | 0.755 |
| 75 | 0.991 | 0.737 |
| 80 | 0.992 | 0.717 |
| 85 | 0.993 | 0.695 |
| 90 | 0.995 | 0.668 |
| 95 | 0.996 | 0.628 |
| 100 | 0.999 | 0.308 |


