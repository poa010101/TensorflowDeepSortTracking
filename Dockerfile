FROM nvidia/cuda:11.6.2-base-ubuntu20.04
MAINTAINER Danny Wang

# Set DEBIAN_FRONTEND to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3-pip python3-dev git wget tar 

RUN pip3 install --upgrade pip
RUN pip3 install tensorflow matplotlib numpy pillow six scipy PyGObject
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

# install Gstreamer lib
RUN apt-get update && apt-get install -y libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-rtsp gir1.2-gst-rtsp-server-1.0 



# Install OpenCV
RUN git clone https://github.com/opencv/opencv.git /opencv
WORKDIR /opencv
RUN mkdir build
WORKDIR /opencv/build
RUN apt-get update && apt-get install -y build-essential cmake unzip 
RUN apt-get update && apt-get install -y libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libusb-1.0-0-dev libudev-dev
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_GSTREAMER=ON -D WITH_GTK=ON ..
RUN make -j4
RUN make install
RUN sudo cp /opencv/build/lib/python3/cv2.cpython-*-gnu.so /usr/local/lib/python3.8/dist-packages/cv2.so
