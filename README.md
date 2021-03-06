# av-stremer

Working with [PyAV](https://github.com/mikeboers/PyAV) and [FFmpeg](https://github.com/FFmpeg/FFmpeg)

Full documentation [PyAV Docs](http://mikeboers.github.io/PyAV/index.html) and [FFmpeg Docs](http://ffmpeg.org/documentation.html)

How install [PyAV Install](http://mikeboers.github.io/PyAV/installation.html)

# Installation example

if  ffmpeg install source code
    
    ./configure --enable-network --enable-protocol=tcp --enable-demuxer=rtsp --enable-decoder=h264
    ./configure --disable-static --enable-shared --disable-doc
    make
    sudo make install

else

    sudo apt-get install ffmpeg x264
    
    sudo apt-get install -y python-dev pkg-config
    
    sudo apt-get install -y \
        libavformat-dev libavcodec-dev libavdevice-dev \
        libavutil-dev libswscale-dev libavresample-dev libavfilter-dev
    
    pip install av
