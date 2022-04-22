# Doorstep Package Recognition 


## Introduction

This project is about an automated doorstep package detection system that uses deep learning to identify multiple classes of packages in real time. An object detection dataset was generated and augmented to make it more robust to adverse weather, motion, and lighting conditions. 

For this project, YOLOv5 object detection model has been trained in AWS and the same model has been deployed on a Kubernetes cluster on the edge for inference. The model has been used to classify packages in a live webcam feed and broadcast the results using a MQTT broker.

## Data

Details about data collection, Annoation and Augmentation are available at: 
- [Data collection, Annotation and Augmentation](https://github.com/jykumari/data-science/tree/main/Deep-Learning-in-cloud-and-edge/Doorstep-package-detection/1-data)

## Model Selection and Training Metrics

Model training details and metrics are available at: 
- [Model Selection and Training Metrics](https://github.com/jykumari/data-science/tree/main/Deep-Learning-in-cloud-and-edge/Doorstep-package-detection/2-model)
- [data.yaml](https://github.com/jykumari/data-science/blob/main/Deep-Learning-in-cloud-and-edge/Doorstep-package-detection/2-model/data.yaml)
- [training Yolov5s](https://github.com/jykumari/data-science/blob/main/Deep-Learning-in-cloud-and-edge/Doorstep-package-detection/2-model/yolov5s.ipynb)

## Inference

- [Using NX](https://github.com/jykumari/data-science/tree/main/Deep-Learning-in-cloud-and-edge/Doorstep-package-detection/3-inference)
- [Container 1 - package-detector](https://github.com/jykumari/data-science/tree/main/Deep-Learning-in-cloud-and-edge/Doorstep-package-detection/3-inference/1-package-detector)
- [Container 2 - package-broker](https://github.com/jykumari/data-science/tree/main/Deep-Learning-in-cloud-and-edge/Doorstep-package-detection/3-inference/2-package-broker)
- [Container 3 - package-logger](https://github.com/jykumari/data-science/tree/main/Deep-Learning-in-cloud-and-edge/Doorstep-package-detection/3-inference/3-package-logger)
- [Inference](https://github.com/jykumari/data-science/tree/main/Deep-Learning-in-cloud-and-edge/Doorstep-package-detection/3-inference/inference-images)
- [Readme_NX_Instructions](https://github.com/jykumari/data-science/blob/main/Deep-Learning-in-cloud-and-edge/Doorstep-package-detection/3-inference/README.md)

## Reports
- [Reports and Presentation](https://github.com/jykumari/data-science/tree/main/Deep-Learning-in-cloud-and-edge/Doorstep-package-detection/4-report-and-presentation)

