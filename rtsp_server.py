import gi
import sys
import os

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

class TestRtspMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        GstRtspServer.RTSPMediaFactory.__init__(self)

    def do_create_element(self, url):
        # Set up the pipeline
        pipeline_str = "( v4l2src device=/dev/video0 ! video/x-raw,width=640,height=480 ! videoconvert ! x264enc speed-preset=ultrafast tune=zerolatency ! rtph264pay name=pay0 pt=96 )"
        return Gst.parse_launch(pipeline_str)


class LoopingRtspMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, mp4_uri):
        GstRtspServer.RTSPMediaFactory.__init__(self)
        self.mp4_uri = mp4_uri

    def do_create_element(self, url):
        # Set up the pipeline
        pipeline_str = f"( uridecodebin uri={self.mp4_uri} ! videoconvert ! x264enc speed-preset=ultrafast tune=zerolatency ! rtph264pay name=pay0 pt=96 )"
        return Gst.parse_launch(pipeline_str)


class GstreamerRtspServer():
    def __init__(self, mp4_path):
        # Initialize GStreamer
        Gst.init(None)

        # Create RTSP server
        self.rtsp_server = GstRtspServer.RTSPServer.new()
        self.rtsp_server.set_service('5000')

        # Create Mount Points
        mounts = self.rtsp_server.get_mount_points()
        factory = TestRtspMediaFactory()
        factory.set_shared(True)
        mounts.add_factory("/test", factory)

        # Create a new factory for the MP4 file
        mp4_uri = "file://" + os.path.abspath(mp4_path)
        mp4_factory = LoopingRtspMediaFactory(mp4_uri)
        mp4_factory.set_shared(True)
        mounts.add_factory("/mp4", mp4_factory)

        # Attach the server to default maincontext
        self.rtsp_server.attach(None)

    def run(self):
        print("\n\nRTSP server is running at rtsp://127.0.0.1:5000/test\n\n")
        print("\n\nMP4 RTSP server is running at rtsp://127.0.0.1:5000/mp4\n\n")
        loop = GObject.MainLoop()
        loop.run()


if __name__ == "__main__":
    s = GstreamerRtspServer("KJ-Run.mp4")
    s.run()
