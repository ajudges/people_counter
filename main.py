"""People Counter."""
"""
 Copyright (c) 2018 Intel Corporation.
 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit person to whom the Software is furnished to do so, subject to
 the following conditions:
 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import os
import sys
import time
import socket
import json
import cv2

import logging as log
import paho.mqtt.client as mqtt

from argparse import ArgumentParser
from inference import Network

#import imutils

# MQTT server environment variables
HOSTNAME = socket.gethostname()
IPADDRESS = socket.gethostbyname(HOSTNAME)
MQTT_HOST = IPADDRESS
MQTT_PORT = 3001
MQTT_KEEPALIVE_INTERVAL = 60


labels = ["background","person", "bicycle", "car", "motorcycle", "airplane", "bus",
    "train", "truck", "boat", "traffic light", "fire hydrant", 
   "stop sign", "parking meter", "bench", "bird", "cat", "dog", 
   "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", 
   "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", 
   "skis", "snowboard", "sports ball", "kite", "baseball bat", 
   "baseball glove", "skateboard", "surfboard", "tennis racket", 
   "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", 
   "banana", "apple", "sandwich", "orange", "broccoli", "carrot", 
   "hot dog", "pizza", "donut", "cake", "chair", "couch", 
   "potted plant", "bed", "dining table", "toilet", "tv", "laptop", 
   "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", 
   "toaster", "sink", "refrigerator", "book", "clock", "vase", 
   "scissors", "teddy bear", "hair drier", "toothbrush"]

def build_argparser():
    """
    Parse command line arguments.

    :return: command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument("-m", "--model", required=True, type=str,
                        help="Path to an xml file with a trained model.")
    parser.add_argument("-i", "--input", required=True, type=str,
                        help="Path to image or video file")
    parser.add_argument("-l", "--cpu_extension", required=False, type=str,
                        default=None,
                        help="MKLDNN (CPU)-targeted custom layers."
                             "Absolute path to a shared library with the"
                             "kernels impl.")
    parser.add_argument("-d", "--device", type=str, default="CPU",
                        help="Specify the target device to infer on: "
                             "CPU, GPU, FPGA or MYRIAD is acceptable. Sample "
                             "will look for a suitable plugin for device "
                             "specified (CPU by default)")
    parser.add_argument("-pt", "--prob_threshold", type=float, default=0.5,
                        help="Probability threshold for detections filtering"
                        "(0.5 by default)")
    return parser

# draw boxes
def draw_boxes(frame, result, args, width, height):
    '''
    Draw bounding boxes onto the frame.
    '''
    count = 0
    for box in result[0][0]: # Output shape is 1x1x100x7
        conf = box[2]
        detected_object = labels[int(box[1])]
        print(detected_object)

        #print(conf)
        if conf >= args.prob_threshold and "person" in detected_object:
            xmin = int(box[3] * width)
            ymin = int(box[4] * height)
            xmax = int(box[5] * width)
            ymax = int(box[6] * height)
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255,0,0), 1)
            count =+1
    return frame, count

def connect_mqtt():
    ### TODO: Connect to the MQTT client ###
    client = None

    return client


def infer_on_stream(args, client):
    """
    Initialize the inference network, stream video to network,
    and output stats and video.

    :param args: Command line arguments parsed by `build_argparser()`
    :param client: MQTT client
    :return: None
    """
    
    present_count=0
    preceding_count=0
    total_count=0
    start_time=0
    duration=0
    frame_count=0
    
    # Initialise the class
    infer_network = Network()
    # Set Probability threshold for detections
    args.prob_threshold = float(args.prob_threshold)

    ### TODO: Load the model through `infer_network` ###
    infer_network.load_model(args.model,args.device, args.cpu_extension)
    rfcnn_input_shape = infer_network.get_input_shape()
    print(rfcnn_input_shape)
    # width and height input to the model
    dsize = (rfcnn_input_shape[3],rfcnn_input_shape[2])


    ### TODO: Handle the input stream ###
    input_stream = cv2.VideoCapture(args.input)
    input_stream.open(args.input)
    
    width = int(input_stream.get(3))
    height = int(input_stream.get(4))
    
    # Create a video output to see your result
    out = cv2.VideoWriter('out.mp4',0x00000021,30,(width,height))

    ### TODO: Loop until stream is over ###
    while input_stream.isOpened():
        ### TODO: Read from the video capture ###
        flag, frame = input_stream.read()
        if not flag:
            break
        key_pressed = cv2.waitKey(60)

        ### TODO: Pre-process the image as needed ###
        p_frame = cv2.resize(frame, dsize)
        p_frame = p_frame.transpose((2,0,1))
        p_frame = p_frame.reshape(1,*p_frame.shape)
        ### TODO: Start asynchronous inference for specified request ###
        infer_network.exec_net(p_frame)

        ### TODO: Wait for the result ###
        if infer_network.wait()==0:
            
            ### TODO: Get the results of the inference request ###
            infer_result = infer_network.get_output()
            
            # update the frame to include results
            frame, present_count = draw_boxes(frame, infer_result, args, width, height)
            
            # when a person is in the video
            if present_count>preceding_count:
                start_time=time.time()
                total_count+=present_count - preceding_count
                frame_count = 0
                print("total count is ", total_count)
            # when there is one less person
            if present_count<preceding_count and frame_count < 60:
                present_count=preceding_count
                frame_count+=1
            # when there is one less person for up to 30 frames
            if present_count<preceding_count and frame_count==60:
                duration = int(time.time() - start_time)
                #print("duration is ", duration)
            preceding_count=present_count
            print("total count", total_count)
            #out.write(frame)
        print("total_count", total_count)
        if key_pressed == 27:
            break
    # -- release the out writer, capture and destroy any opencv windows
    out.release()
    input_stream.release()
    cv2.destroyAllWindows()

            ### TODO: Extract any desired stats from the results ###

            ### TODO: Calculate and send relevant information on ###
            ### current_count, total_count and duration to the MQTT server ###
            ### Topic "person": keys of "count" and "total" ###
            ### Topic "person/duration": key of "duration" ###

        ### TODO: Send the frame to the FFMPEG server ###

        ### TODO: Write an output image if `single_image_mode` ###


def main():
    """
    Load the network and parse the output.

    :return: None
    """
    # Grab command line args
    args = build_argparser().parse_args()
    # Connect to the MQTT server
    client = connect_mqtt()
    # Perform inference on the input stream
    infer_on_stream(args, client)


if __name__ == '__main__':
    main()
