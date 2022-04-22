
### Goal:

The goal of this project is to train an image classification network on the ImageNet dataset to the Top 1 accuracy of 60% or higher.

PyTorch framework have been used for the training.

### The steps:

**I. Procure a virtual machine in AWS** - a T4 GPU and 1 TB of space (e.g. g4dn.2xlarge)has been used for this project.
 Use the Nvidia Deep Learning AMI so that the pre-requisites are pre-installed.

**II. Data download** - Download the ImageNet dataset to your VM.

Data downloading - Training and test data:

curl https://w251hw05.s3-us-west-1.amazonaws.com/ILSVRC2012_img_train.tar --output ILSVRC2012_img_train.tar

curl https://w251hw05.s3-us-west-1.amazonaws.com/ILSVRC2012_img_val.tar --output ILSVRC2012_img_val.tar


**III. Prepare the dataset:**

- create train and val subdirectories and move the train and val tar files to their respective locations
- untar both files and remove them as you no longer need them
- Use the following shell script to process your val directory. It simply moves your validation set into proper subfolders
- When you untarred the train file, it created a large number (1000) of tar files, one for each class. You will need to create a separate directory for each of class , move the tar file there, untar the file and remove it. This should be a one liner shell script
- Make sure that under the train and val folders, there is one directory for class and that the samples for that class are under that directory

*Scripts for the data manipulation part:*

Manipulation for validation file:

mkdir val && mv ILSVRC2012_img_val.tar val/ && cd val && tar -xvf ILSVRC2012_img_val.tar
wget -qO- https://raw.githubusercontent.com/soumith/imagenetloader.torch/master/valprep.sh | bash
ls | wc -l

Manipulation for train file:

cd /data
mkdir train && mv ILSVRC2012_img_train.tar train/ && cd train
tar -xvf ILSVRC2012_img_train.tar && rm -f ILSVRC2012_img_train.tar
find . -name "*.tar" | while read NAME ; do mkdir -p "${NAME%.tar}"; tar -xvf "${NAME}" -C "${NAME%.tar}"; rm -f "${NAME}"; done

**IV. Start training && observe progress!**

### Model setup:
- Architecture used: resnet50
- Optimizer used: SGD
- What should the learning rate and lr_decay be? learning rate set to drop 10x every 33% of training time.
- When to stop training? the bar has been purposefully set at 60% Top1 (on the validation set) so as to avoid the need to choose a very heavy model and / or train it for a very long time.
