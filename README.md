# Real-time Video Streaming Object Tracking (Rstreamer) using GStreamer, SSD Model,  Deep SORT and Tensorflow


## Introduction

This repository is an implementation to perform realtime tracking with Tensorflow using a [SSD model trained on the COCO dataset](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md). It is based on the *Simple Online and Realtime Tracking with a Deep Association Metric* [Deep SORT](https://github.com/nwojke/deep_sort) algorithm. See the original repository for more information.

![alt text](https://github.com/omarabid59/TensorflowDeepSortTracking/blob/master/output_9Diy2e.gif)

## Dependencies
We used following AI model

1. [SSD Model](http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2018_01_28.tar.gz)
2. [Deep SORT](https://github.com/nwojke/deep_sort) are installed.
3. [Label Map](https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/mscoco_label_map.pbtxt)


Your directory structure should look something like this:
```
  ObjectTracking/
  threads/
  utilities/
  README.md
  object_tracking.py
  frozen_inference_graph.pb
  mscoco_label_map.pbtxt

##Setup source rtsp server using webcam as source on host machine##########

sudo apt-get update && apt-get install -y libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-rtsp gir1.2-gst-rtsp-server-1.0
sudo python3 rtsp_server.py

## Setup Docker for sink############
sudo docker buildx build -t rstreamer .
sudo docker run --privileged -it --device=/dev/video1:/dev/video0 --net=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /app:/app rstreamer
"""""""""Inside docker""""""""""""""
export DISPLAY=:1
xvfb-run -s "-screen 0 1280x1024x24" python3 object_tracking.py --input burks-catch.mp4
xvfb-run -s "-screen 0 1280x1024x24" python3 object_tracking.py --input rtsp://127.0.0.1:5000/test
""""""""""""""""""""""""

## Basic Usage
Run the file in your terminal by typing in ```python object_tracking.py```. The script will open up your webcam feed and begin detecting and tracking. The bounding boxes with the class labels are the result of detection from the SSD model. The overlayed blue bounding boxes are the output of the DeepSORT tracker.

If everything goes well, the system should be tracking in real time. Simply press ```Q``` to exit.

- As requested by some individuals, I've added an option to use video input instead of the webcam. Do so by typing `python object_tracking.py --input VIDEO_FILE.mp4`. By default, the video is set to constantly loop through. See the `threads/ImageInput/VideoThread.py` file for implementation.
- Removed the Tensorflow Research [See here](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md) dependencies. Instead, the file required from this repository is copied and can be found at `utilities/external/visualization.py`. I do not take credit for this file!
- I took over the code and made it upto date.I fixed all the lib issues.
Add result output into results.log file as well as CLI.

## Issues
No issues found thus far, but please report any.
