# The Data
The data for this project consists of 865 training images of packages on doorsteps 
## Data Sources
### Roboflow
The first preexisting dataset that our team used was the open-source, user-generated Roboflow [Packages Dataset](https://public.roboflow.com/object-detection/packages-dataset). This dataset consists of 26 raw images of packages on doorsteps that have been augmented with the Roboflow toolkit to generate 250 images labeled with a single `package` class in YOLO format. Our team will use this data to obtain a baseline single-class accuracy to inform our goal accuracy for this project.  
  
An example image from this dataset is below:   

![](images/roboflow.png?raw=true)
  
### Abhijeet Bhatikar
The second preexisting dataset that our team used was from Abhijeet Bhatikar's [package-monitor](https://github.com/abhatikar/package-monitor) project Github repository. This dataset consists of over 500 images of packages on doorsteps in a variety of positions, angles, and lighting conditions labeled with a single `package` class in YOLO format.  
  
An example image from this dataset is below:  
  
![](images/abhijeet.png?raw=true)

### Self-Generated
Our team supplemented the two preexisting datasets with a number of package images of our own creation in the environment in which this project will eventually be deployed. We generated these images by doing the following:  
- Captured several, short videos of doorstep packages, bags, and envelopes in a variety of angles, positions, and lighting conditions. 
- Extracted individual frames from the videos using [ffmpeg](http://ffmpeg.org/).
- Labeled a portion of the extracted frames using [makesense.ai](https://www.makesense.ai/).  
  
Some sample images from this dataset are below:  
  
![](images/self.png?raw=true) 

## Classes
We detemined early on that we wanted our model to have the ability to differentiate multiple types of packages from one another. For this reason, we relabeled both the preexisting datasets and our own data to cover three common classes of packages.

| Class      | Description |
| ----------- | ----------- |
| `box`      | Any rectangular cardboard package that holds its own shape rather than assuming the approximate shape of the object inside.       |
| `plastic_bag`   | Any soft plastic wrapping that does not hold its own shape and roughly assumes the shape of its contects        |
| `envelope`   | Any flat, rectangular packaging made of thick paper or thin cardboard with a single defined opening that is only designed to transport paper, thin books, or other flat objects.        |

## Annotation
All images were labeled using [makesense.ai](https://www.makesense.ai/), a freely available image annotation tool for object detection. Our team divided up the training images, labeled them, and exported the annotations in YOLOv5 format.

An example of an annotated image is below:  
  
![](images/annotations.png?raw=true)

## Augmentation
The dataset was augmented with a simple python script using the albumentations package in order to make the model more resistant to diverse lighting, motion, and weather conditions. The repository file data-aug.py reads all image files in a training directory, augments them with one of three transformation functions, and saves them to a new directory with a new corresponding annotation file in YOLOv5 format. For this project, we used data augmentation to generate a 10x increase in the number of example images in our training dataset.  

| Category| Transformation|
| ----------- | ----------- |
| Lighting      | RGBShift \ RandomBrightnessContrast       |
| Motion   | MotionBlur        |
| Weather | RandomFog \ RandomRain \ RandomSnow \ RandomSunFlare        |  
  
Some examples of augmented images are below:  
  
![](images/aug-examples.png?raw=true)