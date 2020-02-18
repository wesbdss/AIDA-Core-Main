FROM tensorflow/tensorflow:1.14.0-gpu-py3

#
# Criando Diretório Principal
#
RUN mkdir src
WORKDIR /src

#
# Adicionar os arquivos necessários
#
ADD database/data.pickle .
ADD process.py .
ADD requeriments.txt . 

#
# Instalar os requeriments
#
RUN pip3 install --upgrade pip
RUN pip3 install -r requeriments.txt

#
# Rodar o arquivo
#
CMD [ "python3","process.py" ]
