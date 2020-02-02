FROM tensorflow/tensorflow:1.15.0rc1-py3

RUN mkdir ./homework
ADD ./intents.json ./homework/
ADD ./program.py ./homework/
ADD ./requeriments.txt ./homework/
WORKDIR ./homework/
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requeriments.txt
# RUN python -m "import nltk; nltk.download('punkt')"

CMD [ "python3","./main.py" ]
