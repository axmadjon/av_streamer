import av


########################################################################################################################

class MyStream:
    def can_mux(self, packet):
        pass

    def mux(self, packet):
        pass


########################################################################################################################

class MyFrameStream(MyStream):
    def __init__(self, output, rate):
        self.__output = output
        self.__stream = self.__output.add_stream(codec_name='mpeg4', rate=rate)
        self.__stream.options = {}

        self.__frame_listener = None

    def frame_listener(self, frame_listener):
        self.__frame_listener = frame_listener

    def set_input(self, input_content):
        stream = input_content.frame_stream()
        self.__stream.pix_fmt = stream.pix_fmt
        self.__stream.width = stream.width
        self.__stream.height = stream.height

    def can_mux(self, packet):
        return packet.stream.type == 'video'

    def mux(self, packet):
        if not self.can_mux(packet) or not self.__stream:
            return

        try:
            for frame in packet.decode():
                cv2_image = frame.to_nd_array(format='bgr24')
                if self.__frame_listener:
                    self.__frame_listener(cv2_image)

                frame = av.VideoFrame.from_ndarray(cv2_image, format='bgr24')
                for packet in self.__stream.encode(frame):
                    self.__output.mux(packet)
        except Exception as e:
            print('Error on run VideoOutput {}'.format(e))


########################################################################################################################

class MyAudioStream(MyStream):
    def __init__(self, output):
        self.__output = output
        self.__stream = self.__output.add_stream(codec_name='mp3')
        self.__stream.options = {}

    def can_mux(self, packet):
        return packet.stream.type == 'audio'

    def mux(self, packet):
        if not self.can_mux(packet) or not self.__stream:
            return

        try:
            for frame in packet.decode():
                frame.pts = None
                for packet in self.__stream.encode(frame):
                    self.__output.mux(packet)

        except Exception as e:
            print('Error on run AudioOutput {}'.format(e))


########################################################################################################################

class MyVideoStream(MyStream):
    def __init__(self, output, fps):
        self.__output = output
        self.__frame_stream = MyFrameStream(self.__output, fps)
        self.__audio_stream = MyAudioStream(self.__output)

    def set_input(self, input_content):
        self.__frame_stream.set_input(input_content=input_content)

    def frame_listener(self, frame_listener):
        self.__frame_stream.frame_listener(frame_listener)

    def can_mux(self, packet):
        return self.__frame_stream.can_mux(packet) or self.__audio_stream.can_mux(packet)

    def mux(self, packet):
        if not self.can_mux(packet):
            return

        if self.__frame_stream.can_mux(packet):
            self.__frame_stream.mux(packet)

        if self.__audio_stream.can_mux(packet):
            self.__audio_stream.mux(packet)


########################################################################################################################

class MyInputStream:
    def __init__(self, input):
        self.__input = input

    def frame_fps(self):
        frame_stream = self.frame_stream()

        if frame_stream:
            return frame_stream.average_rate

        return 25

    def frame_stream(self):
        return next(s for s in self.__input.streams if s.type == 'video')

    def audio_stream(self):
        return next(s for s in self.__input.streams if s.type == 'audio')

    def __mux(self, packet, output_stream):
        if type(output_stream) == list:
            for stream in output_stream:
                if stream.can_mux(packet):
                    stream.mux(packet)

        else:
            if output_stream.can_mux(packet):
                output_stream.mux(packet)

    def run(self, output_stream):
        next(self.__input.decode(video=0))

        videopackets = []
        audiopackets = []

        for packet in self.__input.demux():
            if packet.stream.type == 'video':
                videopackets.append(packet)
                if len(audiopackets) > 0:
                    break

            elif packet.stream.type == 'audio':
                audiopackets.append(packet)
                if len(videopackets) > 0:
                    break

        for packet in videopackets + audiopackets:
            self.__mux(packet=packet, output_stream=output_stream)

        for packet in self.__input.demux():
            self.__mux(packet=packet, output_stream=output_stream)


########################################################################################################################

def start_stream(rtsp_url, output_file, frame_listener=None):
    rtsp_stream = MyInputStream(av.open(rtsp_url, 'r'))
    video_stream = MyVideoStream(av.open(output_file, 'w'), rtsp_stream.frame_fps())

    video_stream.set_input(rtsp_stream)
    video_stream.frame_listener(frame_listener)

    rtsp_stream.run(video_stream)
