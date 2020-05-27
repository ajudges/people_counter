# people_counter
This application is designed to count the number of people and their duration in an environment. It's use cuts across different applications such as counting the number of people in a mall or using it to limit access of people to a place. 

## Guide for running the app
### Prerequisite
- Openvino (You can run [this script](https://github.com/Tob-iee/OpenVINO_installation) to automate the installation of openvino)
- Nodejs and npm 



### Extracting the model
First, download the [ssd_mobilenet_v2_coco model](http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz)
From command line/terminal, navigate to the directory where the model was downloaded and extract it using
'''
tar -xvf ssd_mobilenet_v2_coco_2018_03_29.tar.gz
'''
Go to the just extracted directory (ssd_mobilenet_v2_coco_2018_03_29) and generate the intermediate represention (IR) files i.e.(.xml and .bin) using the model optimizer by running the following
'''
python /opt/intel/openvino/deployment_tools/model_optimizer/mo_tf.py --input_model frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config pipeline.config --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json --reverse_input_channel
'''
Clone this repo and create a "model" directory

Copy the generated .xml and .bin file into the "model" directory

## Running the App




