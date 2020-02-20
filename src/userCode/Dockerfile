FROM tensorflow/tensorflow:1.14.0-gpu-py3

#
# Criando Diretório Principal
#

RUN mkdir src
WORKDIR /src

ADD server.py .
ADD process.py .
ADD database/data.pickle .
ADD database/intents.json .
ADD requerimentsGen.txt .
ADD model .

ADD preprocess.py .
ADD process.py .



RUN pip3 install --upgrade pip
RUN pip3 install -r requerimentsGen.txt

#
# Rodar o arquivo
#

CMD [ "python3","server.py" ]
