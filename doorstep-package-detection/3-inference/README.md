
## INTRODUCTION

Jetson NX has been used for running inference with custom YOLOv5 model trained to detect packages as box, plastic_bags and envelopes on images and videos.

**There are 3 containers for NX:**

1) **package-detector** 
    
    jkumariucb/package-detector:v1 - https://hub.docker.com/repository/docker/jkumariucb/package-detector
    
    Includes:
    
    - a) trained model with weights
    
    - b) package-detector.py and other util files/directories
    
    - c) Dockerfile 
    
    - d) package-detector-deployment.yaml


2) **package-broker**
    
    jkumariucb/package-broker:v1 - https://hub.docker.com/repository/docker/jkumariucb/package-broker
    
    Includes:
    
    - a) Dockerfile
    
    - b) package-broker-deployment.yaml
    
    - c) package-broker-service.yaml (*created a service, to access the broker from outside Kubernetes and then from inside it*)


3) **package-logger**
    
    jkumariucb/package-logger:v1 - https://hub.docker.com/repository/docker/jkumariucb/package-logger
    
    Includes:
    
    - a) Dockerfile
    
    - b) package-logger-deployment.yaml
    
    - c) package-logger.py


***Following changes have been made to adapt trained yolov5s model onto Jeston device***

**Step 1. Adapt Dockerfile from Yolov5s default model for NX**

	- Added new base image in the DockerFile
	- Added new packages to be added to new container: refer to <Dockerfile> for all the packages

**Step 2. Change detect.py from [Yolov5s original model](https://github.com/ultralytics/yolov5) as package-detector.py for running on NX**

	Changes made in package-detector.py:
		- Added msg for MQTT
			- import of mqtt client and connect to local mosquitto service
			- publish the detected objects for message logger to log.
		- Changed default variables of detect.py
			- changed image size from 640 to 416
			- changed default input from folder to webcam
			- changed default confidence threshold from 0.25 to 0.5 in order to show only high confidence detections.


***Please find the complete set of steps below to configure NX:***

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

     cd <PathTo-w251-final-project-3-architecture>/2-package-broker; docker build -t jkumariucb/package-broker:v1 .; docker push jkumariucb/package-broker:v1; cd ../3-package-logger; docker build -t jkumariucb/package-logger:v1 .; docker push jkumariucb/package-logger:v1; cd ../1-package-detector; docker build -t jkumariucb/package-detector:v1 .; docker push jkumariucb/package-detector:v1


**Step 4) Kubernetes**
-----------------------------------

a. To install K3s, run the following:

      mkdir $HOME/.kube/
      curl -sfL https://get.k3s.io | sh -s - --docker --write-kubeconfig-mode 644 --write-kubeconfig $HOME/.kube/config

b. Start Kubernetes

    sudo systemctl start k3s

c. Deploy YAML file, broker and service through Kubectl into Kubernetes:

      cd <PathTo-w251-final-project-3-architecture>/2-package-broker; kubectl apply -f package-broker-deployment.yaml; kubectl apply -f package-broker-service.yaml; cd ../3-package-logger; kubectl apply -f package-logger-deployment.yaml; cd ../1-package-detector; kubectl apply -f package-detector-deployment.yaml

d. Display information about the Deployment:

    kubectl describe deployment <deployment name>

e. Confirm the pod is running:

    kubectl get pods -l app=mosquitto

f. Display some information about a Pod:

    kubectl describe pod <pod-name>

g. Check Pod's logs:

    kubectl logs -f <podName>

h. Confirm if broker service is running and take note of the NodePort Kubernetes assigns.

  Run the command

    'kubectl get service package-broker-service'


----------------------------------------END OF FILE-------------------------------------------------
