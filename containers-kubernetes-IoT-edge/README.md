
## LINKS:
Location of my faces in the object storage: https://myfaceucb.s3-us-west-1.amazonaws.com/image101.png

To  list all the images: https://myfaceucb.s3-us-west-1.amazonaws.com/

## INTRODUCTION

**There are 4 containers for NX:**
1) Face_Detector
    Includes:
    a) Dockerfile
    b) face-detector.yaml
    c) facedetect.py
    d) haarcascade_frontalface_default.xml

2) MQTT_Broker
    Includes:
    a) Dockerfile
    b) mosquitto-broker.yaml
    c) mosquittobrokerService.yaml (*created a service, to access the broker from outside Kubernetes and then from inside it*)

3) Message_Logger
    Includes:
    a) Dockerfile
    b) message-logger.yaml
    c) listener.py

4) MQTT_Message_Forwarder
    Includes:
    a) Dockerfile
    b) message-forwarder.yaml
    c) listener.py

**There are 2 containers for AWS cloud:**
1)  MQTT_Broker_aws
    Includes:
    a) Dockerfile

2) image_processor_aws
    Includes:
    a) Dockerfile
    b) facesave.py

## INSTRUCTIONS FOR CONFIGURING NX:

**Step 1) DOCKER**
----------------------------------------------------

*Run the command to check if things are correctly installed:*

    docker run --rm hello-world

**Step 2) USING Nvidia GPU:**
----------------------------------------------------

Edit the file /etc/docker/daemon.json, e.g. sudo vi /etc/docker/daemon.json, adding/setting the default-runtime to nvidia.

    {
        "runtimes": {
            "nvidia": {
                "path": "nvidia-container-runtime",
                "runtimeArgs": []
            }
        },
        "default-runtime": "nvidia"
    }

Reboot your NX and login when reboot is completed.

Interacting Jetson via an attached display, run

        export DISPLAY=:0

To allow containers to communicate with X, run:

        sudo xhost +

Running Jetpack 4.5

        docker run --rm --network host -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix nvcr.io/nvidia/l4t-base:r32.5.0

Once in the shell, run the following commands:

      apt-get update && apt-get install -y --no-install-recommends make g++
      cp -r /usr/local/cuda/samples /tmp
      cd /tmp/samples/5_Simulations/nbody
      make
      ./nbody

This will display a GPU powered N-body simulation, running in a container and displaying on your UI. Close the window and exit out of your container.

**Step 3) BUILDING CONTAINERS**
----------------------------------------------------

Build all containers and push to DockerHub registry (login to docker using command line)

    docker login

     cd ~/w251-week3/NX/MQTT_Broker; docker build -t jkumariucb/mosquitto-broker:v1 .; docker push jkumariucb/mosquitto-broker:v1; cd ../Message_Logger; docker build -t jkumariucb/message-logger:v1 .; docker push jkumariucb/message-logger:v1; cd ../MQTT_Message_Forwarder; docker build -t jkumariucb/message-forwarder:v1 .; docker push jkumariucb/message-forwarder:v1; cd ../Face_Detector; docker build -t jkumariucb/facedetect:v1 .; docker push jkumariucb/facedetect:v1


**Step 4) Kubernetes**
-----------------------------------

a. To install K3s, run the following:

      mkdir $HOME/.kube/
      curl -sfL https://get.k3s.io | sh -s - --docker --write-kubeconfig-mode 644 --write-kubeconfig $HOME/.kube/config

b. Start Kubernetes

    sudo systemctl start k3s

c. Deploy all the YAML files, broker and the mosquittobroker service through Kubectl into Kubernetes:

      cd ~/w251-week3/NX/MQTT_Broker; kubectl apply -f mosquitto-broker.yaml; kubectl apply -f mosquittobrokerService.yaml; cd ../Message_Logger; kubectl apply -f message-logger.yaml; cd ../MQTT_Message_Forwarder; kubectl apply -f message-forwarder.yaml; cd ../Face_Detector; kubectl apply -f face-detector.yaml

d. Display information about the Deployment:

    kubectl describe deployment <deployment name>

e. Confirm the pod is running:

    kubectl get pods -l app=mosquitto

f. Display some information about a Pod:

    kubectl describe pod <pod-name>

g. Check Pod's logs:

    kubectl logs <podName>

h. Confirm if broker service is running and take note of the NodePort Kubernetes assigns.

  Run the command

    'kubectl get service mosquitto-service'


## INSTRUCTIONS FOR CONFIGURING AWS CLOUD AND S3 STORAGE


**Step 1) Create AWS instance**
---------------------------------
    aws ec2 run-instances --image-id <AMI ID> --instance-type t2.medium --security-group-ids <GroupID> --associate-public-ip-address --instance-market-options file://spot-options.json --key-name <keypair name>

    aws ec2 describe-instances

    aws ec2 describe-instances | grep PublicDnsName


**Step 2) SSH to your cloud VM**
---------------------------------

    ssh -i ./dev.pem ubuntu@ec2-54-241-153-45.us-west-1.compute.amazonaws.com

After that use the following steps to configure AWS CLI on the VM and to have access to your IAM

    ~/.aws/credentials

[default]

aws_access_key_id=<aws_access_key_id>

aws_secret_access_key=<aws_secret_access_key>

    ~/.aws/config

[default]

region=us-west-1

output=json


**Step 3): configure AWS CLI**
---------------------------------

      sudo apt install unzip
      curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
      unzip awscliv2.zip
      sudo ./aws/install
      aws configure


**Step 4): Create a password file using your access key and shared file (what you use in aws configure)**
----------------------------------------------------------------------------------------------------------

      echo <access_key>:<secret key> > ~/.passwd-s3fs
      echo <aws_access_key_id>:<aws_secret_access_key> > ~/.passwd-s3fs
      chmod 400 ~/.passwd-s3fs


**Step 5) Create S3 object storage and mount a directory on the cloud instance. install s3fs**
---------------------------------------------------------------------------------------------------

a. Create a bucket:

    aws s3 mb s3://myfaceucb

b. Check if it  exists:

    aws s3 ls

c. Install s3fs - to mount the bucket to the local directory:

    sudo apt-get update
    sudo apt-get install automake autotools-dev g++ git libcurl4-openssl-dev libfuse-dev libssl-dev libxml2-dev make pkg-config
    git clone https://github.com/s3fs-fuse/s3fs-fuse.git
    cd s3fs-fuse  
    ./autogen.sh
    ./configure
    make
    sudo make install
    which s3fs

d. Create a local mount of the s3 bucket:


    sudo mkdir /mnt/mountpoint/facehw3
    sudo chmod 777 /mnt/mountpoint/facehw3

    /usr/local/bin/s3fs -o url="https://s3.us-west-1.amazonaws.com" -o endpoint=us-west-1 -o dbglevel=info -o allow_other myfaceucb /mnt/mountpoint/facehw3

   If you get below message, Open /etc/fuse.conf and uncomment the last line.
   
   `fusermount: option allow_other only allowed if 'user_allow_other' is set in /etc/fuse.conf`


e. Check if it works

    df -h

   We should see :
   
   `
   s3fs     256T     0  256T   0% /mnt/mountpoint/facehw3`

f. Add a file and check if it appears on the AWS console online:

    cd /mnt/mountpoint/facehw3
    mkdir test
    echo "hello-world" > helloworld.txt


**Step 6) Install docker**
---------------------------------

    sudo su
    apt-get update
    apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        software-properties-common

    add the docker repo    
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
       $(lsb_release -cs) \
       stable"

    install it
    apt-get update
    apt-get install docker-ce


**Step 7) Create a network (i.e. "hw03") so that the cloud-based docker containers can communicate.**
---------------------------------------------------------------------------------------------------

    sudo docker network create hw03


-> Open port 1883 through Aws console and add as an inbound rule.



**Step 8) Create docker image and launch cloud MQTT Broker container.**
---------------------------------------------------------------------------------------------------

The Dockerfile is located in the w251-week3/AWS-CLOUD/MQTT_Broker_aws directory. Note: upon running this container, Mosquitto will be launched automatically.


Docker build, push and run for cloud broker container:

- Build and tag the image:

        sudo docker build -t jkumariucb/mosquitto-broker-aws:v1 .

- Push it into your DockerHub registry:

        sudo docker push jkumariucb/mosquitto-broker-aws:v1

- Run broker container:

        sudo docker run -it --name mosquitto -p 1883:1883 --network hw03 jkumariucb/mosquitto-broker-aws:v1


**Step 9) Create docker image and launch image processor container in the aws cloud.**
---------------------------------------------------------------------------------------------------

The Dockerfile is located in the w251-week3/AWS-CLOUD/image_processor_aws directory. The first volume (-v) command in the docker run script will give you access to the s3 mounted directory for storing new files. The working directory (-w /app) command will launch the container directly into the appropriate directory to access the script, facesave.py


Docker build, push and run for Image Processor:

 - Build and tag the image:

        sudo docker build -t jkumariucb/facesave:v1 .

- Push it into your DockerHub registry:

        sudo docker push jkumariucb/facesave:v1

- Run image processor container:

        sudo docker run -it --name facesave --network hw03 -v /mnt/mountpoint/facehw3:/mnt/mountpoint/facehw3 -v /w251-week3/AWS-CLOUD/image_processor_aws/:/app/ -w /app/  jkumariucb/facesave:v1



                         
    --------------------------------------------------------END OF FILE----------------------------------------------------
