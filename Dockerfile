FROM nvidia/cuda:11.6.2-base-ubuntu20.04
MAINTAINER Danny Wang

# Set DEBIAN_FRONTEND to noninteractive
ENV DEBIAN_FRONTEND=noninteractive



RUN apt-get update && apt-get install -y python3-pip python3-dev git wget tar

RUN pip3 install --upgrade pip
RUN pip3 install tensorflow opencv-python matplotlib numpy pillow six scipy
RUN git clone https://github.com/poa010101/TensorflowDeepSortTracking.git tf_tracking
WORKDIR /tf_tracking
RUN wget https://arkansasrazorbacks.com/wp-content/uploads/2021/11/KJ-Run.mp4
RUN wget https://arkansasrazorbacks.com/wp-content/uploads/2021/11/burks-catch.mp4
RUN wget http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2018_01_28.tar.gz
RUN wget https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/mscoco_label_map.pbtxt
RUN gunzip -k ssd_inception_v2_coco_2018_01_28.tar.gz
RUN chmod +x ssd_inception_v2_coco_2018_01_28.tar
RUN tar -xf ssd_inception_v2_coco_2018_01_28.tar
RUN mv ./ssd_inception_v2_coco_2018_01_28/frozen_inference_graph.pb .
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 libxcb1  libxcb-xinerama0 libxcb-shm0 libxcb-shape0 libxcb-xfixes0 xvfb

