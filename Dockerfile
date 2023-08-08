FROM devuan/devuan:chimaera

RUN apt-get -q update
RUN apt-get install -qqqy python3-pip ffmpeg git-core

RUN pip3 install numba==0.56.0 openai openai-whisper requests
RUN pip3 install PyYAML kizano

RUN pip3 install git+https://github.com/markizano/auto-subtitle

# Convince openai-whisper to go ahead and download an English model.
RUN python3 -c 'import whisper; whisper.load_model("base"); whisper.load_model("small")'
ENTRYPOINT ["/usr/local/bin/auto_subtitle"]
CMD ["# (noop)"]
