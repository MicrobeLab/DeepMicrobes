# How to submit to GPUs

No codes or configurations should be modified to submit to GPUs. 

However, we noticed that TensorFlow attempts to occupy memory of all GPU devices (on a compute node) that are visible to it, even though only one device is actually running the model. 

To avoid this, you could manually set the variable `CUDA_VISIBLE_DEVICES`. 

Suppose that we have two datasets `sample_A.tfrec` and `sample_B.tfrec` and we would like to respectively submit them to `GPU 0` and `GPU 1` on a compute node.

<b>The submission script for `sample_A` should look like:</b>
```sh
export CUDA_VISIBLE_DEVICES=0  # GPU 0
predict_DeepMicrobes.sh -i sample_A.tfrec -m model_dir -o sample_A  # sample_A
```

<b>The submission script for `sample_B` should look like:</b>
```sh
export CUDA_VISIBLE_DEVICES=1  # GPU 1
predict_DeepMicrobes.sh -i sample_B.tfrec -m model_dir -o sample_B  # sample_B
```

