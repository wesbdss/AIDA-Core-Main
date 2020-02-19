FROM tensorflow/tensorflow:1.14.0-gpu-py3

#
# Criando Diretório Principal
#

EXPOSE 10101:10101
RUN mkdir src
WORKDIR /src

ADD serve.py .
ADD process.py .
ADD database/data.pickle .
ADD database/intents.json .
ADD requerimentsGen.txt .
ADD model .


RUN pip3 install --upgrade pip
RUN pip3 install -r requerimentsGen.txt

#
# Rodar o arquivo
#

CMD [ "python3","serve.py" ]
