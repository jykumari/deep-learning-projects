
This repository contains all files and folders related to aspects of multi-node and multi-gpu (mnmg) model training.


# Distributed training

**Goal:**
Run multi-node training on imagenet dataset on two GPU nodes instead of one.

# Steps

**Step I - Set up AWS instance**

*A. Set up AWS instances and ssh to cloud VM:*

  - Launch two g4dn.2xlarge instances
  - Add 2 instances - 8 vCPUs - Use the Nvidia Deep Learning AMI

  - Increase storage to 1023GB
  - Security group- open up all TCP ports (0-65535)

*B. ssh to AWS cloud VM:*

    ssh -i ./dev.pem ubuntu@ec2-3-101-111-25.us-west-1.compute.amazonaws.com

    ssh -i ./dev.pem ubuntu@ec2-13-57-177-94.us-west-1.compute.amazonaws.com


**STEP II: Set up data**

Repeat below steps in both the instances

*A. Check if volume is created:*

      df -v

*B. Create a data directory in AWS instance*

      sudo mkdir /data

      sudo chown ubuntu:ubuntu /data

      cd /data

      ls -al

*C. Data downloading - Training and test data:*

      curl https://w251hw05.s3-us-west-1.amazonaws.com/ILSVRC2012_img_train.tar --output ILSVRC2012_img_train.tar

      curl https://w251hw05.s3-us-west-1.amazonaws.com/ILSVRC2012_img_val.tar --output ILSVRC2012_img_val.tar


*D. Data manipulation part:*

Use below scripts for data manipulation:

Manipulation for validation file:

      mkdir val && mv ILSVRC2012_img_val.tar val/ && cd val && tar -xvf ILSVRC2012_img_val.tar;
      wget -qO- https://raw.githubusercontent.com/soumith/imagenetloader.torch/master/valprep.sh | bash; ls | wc -l

Manipulation for train file:

      cd /data;
      mkdir train && mv ILSVRC2012_img_train.tar train/ && cd train;
      tar -xvf ILSVRC2012_img_train.tar && rm -f ILSVRC2012_img_train.tar;
      find . -name "*.tar" | while read NAME ; do mkdir -p "${NAME%.tar}"; tar -xvf "${NAME}" -C "${NAME%.tar}"; rm -f "${NAME}"; done

cd ..

Make an app directory:

      sudo mkdir /app

      sudo chown ubuntu:ubuntu /app

**STEP III: Docker and jupyter notebooks**

*A. Spin up a docker container:*

      docker pull nvcr.io/nvidia/pytorch:21.06-py3

For all ports:

      docker run --gpus all --shm-size=2048m --rm --ipc=host --net=host -v /data:/data -v /app:/app -ti nvcr.io/nvidia/pytorch:21.06-py3 bash

*B. Open Jupyter notebook:*

      jupyter lab --ip=0.0.0.0 --allow-root

*C. Run below ipynb files:*

Below notebooks includes commands for: Pytorch DDP and Pytorch Native AMP.

It has been demonstrated that the distributed training using two GPUs is ~2x faster than on a single GPU machine.

Wall time for single GPU machine: 57min 32s

  - [homework09-1GPU.ipynb](https://github.com/jkumariucb/w251-hw09/blob/main/homework09-1GPU.ipynb)

Wall time with DDP (Distribute Data-Parallel Training): 31min 18s

  - [homework09-ddp-1.ipynb](https://github.com/jkumariucb/w251-hw09/blob/main/homework09-ddp-1.ipynb)
  - [homework09-ddp-2.ipynb](https://github.com/jkumariucb/w251-hw09/blob/main/homework09-ddp-2.ipynb)


*D. Monitor the GPU utilization using nvidia-smi (Recommended)*

# Output:

*Below two files show that GPU utilization on both instances are > 95%*

  - [GPU1-utilization.png](https://github.com/jkumariucb/w251-hw09/blob/987b07045eda3f12324d42b188788adfa76f3df4/GPU1-utilization.png)
  - [GPU2-utilization.png](https://github.com/jkumariucb/w251-hw09/blob/main/GPU2-utilization.png)

*Visualization using Tensorboard and Weights & Biases:*

  - [tensorboard_visualization](https://github.com/jkumariucb/w251-hw09/blob/main/tensorboard_visualization.ipynb)
  - [Homework 9 - Distributed training – Weights & Biases.pdf](https://github.com/jkumariucb/w251-hw09/blob/main/Homework%209%20-%20Distributed%20training%20%E2%80%93%20Weights%20%26%20Biases.pdf)

*Run using Tensorboard or Weights and Biases*

  - [Run using Tensorboard or Weights and Biases](https://github.com/jkumariucb/w251-hw09/tree/main/run)
