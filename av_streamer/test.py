from threading import Thread
from time import sleep

from av_streamer import start_stream


def frame(image):
    print(len(image))


def connect_camera():
    start_stream('rtsp://192.168.10.210/Streaming/Channels/1', '/home/smartup/z_test_ffmpeg/test.mp4', frame)

    print('reconnect at 5 second')
    sleep(5)
    print('reconnect')
    Thread(target=connect_camera).start()


Thread(target=connect_camera).start()
