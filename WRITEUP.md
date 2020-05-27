# Project Write-Up

There is an increase in the use of computer vision applications on the edge (near the data source). The models for these computer vision applications are usually built with a variety of different frameworks such as Tensorflow, Pytorch etc. Deploying models from these frameworks across different hardwares not only requires a significant level of expertise, the differences in the various hardwares also ensure that the models are not optimized to run at a high performance. 

OpenVINO toolkit helps solves the problem of different frameworks and hardwares. It is a toolkit developed by INTEL to accelerate the development of deep learning applications by converting models from different frameworks into a unified intermediate representation format and also optimizes the models for the hardware (Intel) they are run on.

This project "Deploying a people counter at the edge," shows the benefits of using OpenVINO, by deploying a tensorflow object detection model ([SSD MobileNet v2 Coco](http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz)) on a CPU running on Intel hardware.   

## Explaining Custom Layers
OpenVINO toolkit uses the model optimizer to convert the known layers in a model into corresponding internal representation, optimizing the model and produces a set of intermediate representation files. However, some devices may not support all of the layers in a model. The layers not supported by the devices are usually classified as unsupported layers. Hence, the need for custom layers.    

The process behind converting custom layers involves a preliminary check for unsupported layers using model and the device type, via the query_network method on the IECore class. If there are unsupported layers, a custom layer can then be added with the add_extension method using the required library and deployment device type. 

Some of the potential reasons for handling custom layers are...

## Comparing Model Performance

My method(s) to compare models before and after conversion to Intermediate Representations
were by comparing the size and inference time of the model pre- and post-conversion. 

The difference between model accuracy pre- and post-conversion was...

The size of the model pre-conversion is 69.7 MB, while the post-conversion size is 67.4 MB.

The average inference time of the model pre-conversion is 181.5 ms and the average post-conversion inference time  is 75 ms.

## Assess Model Use Cases

Some of the potential use cases of the people counter app are (1) checking the number of participants in an event such as a lecture. (2) limiting the number of people that can enter an environment at a particular time.

Checking the number of participants in an event with this system, eliminates the need for manual recording of attendees. This can help generate insights on which events people turn up for most. In addition, it can be used to keep track of the duration of the event. 

The second use case can be very useful, especially in limiting the spread of infectious diseases by monitoring the amount of people that can enter a particular space at a time e.g. a mall. For instance, it can be used to only allow one person to enter into a location within a given time frame.

## Assess Effects on End User Needs

No model is hundred percent accurate. The model deployed in this project has a mean average precision of 22 COCO mAP(^1). It could be seen that the model was not always identifying a particular person who was dressed in an all black attire and had his hair styled in a particular unique way. 

The model would perform poorly in poor lighting conditions. The model should not be expected to detect people when the ambience is dark. 