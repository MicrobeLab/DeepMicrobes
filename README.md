# DeepMicrobes
DeepMicrobes: taxonomic classification for metagenomics with deep learning

## Installation

#### Dependencies
DeepMicrobes relies on the following Python modules:
* biopython
* numpy
* tensorflow
* absl

#### Clone
To start working with the code:

    git clone https://github.com/MicrobeLab/DeepMicrobes.git
    
## Usage

#### Training

    python DeepMicrobes.py --train_epochs=${EPOCH} --batch_size=${BATCH_SIZE} \
                           --lr=${LEARNING_RATE} --lr_decay=${LEARNING_RATE_DECAY} \
                           --num_classes=${NUM_CLASSES} --keep_prob=${KEEP_PROB} \
                           --input_tfrec=${TFRECORD} --model_dir=/path/to/weights \
                           --running_mode=train --model_name=attention
                           
#### Evaluation

    python DeepMicrobes.py --batch_size=${BATCH_SIZE} --num_classes=${NUM_CLASSES} \
                           --input_tfrec=${TFRECORD} --model_dir=/path/to/weights \
                           --running_mode=eval --model_name=attention
                           

#### Prediction

For paired-end data:
    
    python DeepMicrobes.py --batch_size=${BATCH_SIZE} --num_classes=${NUM_CLASSES} \
                           --input_tfrec=${TFRECORD} --model_dir=/path/to/weights \
                           --label_file=/path/to/label2taxid.txt --translate=True \
                           --pred_out=/path/to/pred_out_prefix \
                           --running_mode=predict_paired_class --model_name=attention

For single-end data:

    python DeepMicrobes.py --batch_size=${BATCH_SIZE} --num_classes=${NUM_CLASSES} \
                           --input_tfrec=${TFRECORD} --model_dir=/path/to/weights \
                           --label_file=/path/to/label2taxid.txt --translate=True \
                           --pred_out=/path/to/pred_out_prefix \
                           --running_mode=predict_single_class --model_name=attention
                           
#### Report
                           
To summarize read-level predictions into a community report:

    paste pred_out_prefix.category_[paired/single].txt pred_out_prefix.prob_[paired/single].txt > ${PREDICT_RESULT}
    python community_profile.py -i=${PREDICT_RESULT} -o=${SAMPLE_OUTPUT} \
                                -t=/path/to/name2taxid.txt
                                
#### Visualization

To visualize the attention score of the ${INDEX}th sequence in ${SEQ_FASTA}:

    python visualize_attention.py -s=${SEQ_FASTA} -a=${ATTENTION_MATRIX} \
                                  -o=${OUTPUT_HTML} -i=${INDEX}
                                  
                                  
## Contact

Any issues with the DeepMicrobes framework can be filed with [GitHub issue tracker](https://github.com/MicrobeLab/DeepMicrobes/issues).
