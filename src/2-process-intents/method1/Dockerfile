FROM tensorflow/tensorflow:1.15.0rc1-py3

RUN mkdir src

WORKDIR /src

ADD data.pickle .

ADD process.py .


CMD [ "python3","./main.py" ]
