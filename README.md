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

From terminal, navigate to the cloned root directory and give permission to the script to install the required modules (i.e. nodejs, ffserver) for Mac and/or Linux with the following command 

'''
chmod +x setup.sh
'''

Run the script using

'''
./setup.sh
'''

## Running the App
Four terminal windows will be needed to run the app.

### Start the Mosca Server on the first terminal window
'''
cd <app_dir>/webservice/server/node-server
node ./server.js
'''

If successful, the following message should appear
'''
connected to ./db/data.db
Mosca server started.
'''

### Start the UI on the second terminal Window
Open new terminal (i.e. second terminal) and run the commands below

'''
cd <app_dir>/webservice/ui
npm run dev
'''

If successful, the following message should appear
'''
webpack: Compiled successfully
'''

### Start the FFmpeg Server on the third terminal Window
Open the third terminal and run the commands below

'''
cd <app_dir>
sudo ffserver -f ./ffmpeg/server.conf
'''

### Running the program on the fourth terminal 
First, initialize the Openvino environment by running the command below

'''
source /opt/intel/openvino/bin/setupvars.sh -pyver 3.5
'''

#### To capture from video, 
On the same terminal (i.e. the fourth terminal), run: 

'''
python3 main.py -i <location of video> -m model/frozen_inference_graph.xml -d GPU -pt 0.6 | ffmpeg -v warning -f rawvideo -pixel_format bgr24 -video_size 768x432 -framerate 24 -i - http://0.0.0.0:3004/fac.ffm
'''

#### To capture from camera,
On the same terminal (i.e. the fourth terminal), run: 

'''
python3 main.py -i 0 -m model/frozen_inference_graph.xml -d GPU -pt 0.6 | ffmpeg -v warning -f rawvideo -pixel_format bgr24 -video_size 768x432 -framerate 24 -i - http://0.0.0.0:3004/fac.ffm
'''

## View Output
To see the output on a web based interface, open the link http://0.0.0.0:3004 in a browser.
