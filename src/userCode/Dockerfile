FROM tensorflow/tensorflow:1.14.0-gpu-py3

#
# Criando Diretório Principal
#

RUN mkdir src
WORKDIR /src

RUN mkdir libs
RUN mkdir arquivos
ADD libs libs/
ADD arquivos arquivos/
ADD requerimentsGen.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requerimentsGen.txt

ADD server.py .

#
# Rodar o arquivo
#

CMD [ "python3","server.py" ]
