FROM python:3.6.8-slim

#
# Criando diretorios do método
#

RUN mkdir src
WORKDIR /src

ADD preprocess.py .
ADD requeriments.txt .

#
# Criando diretorio dos database
#

RUN mkdir database

ADD database/intents.json database/

#
# Criando diretorio dos utils
#

RUN mkdir utils

ADD utils/findImports.py utils/

#
# Instalando dependências
#

RUN pip install --upgrade pip
RUN pip install -r requeriments.txt

#
# Rodando o container
#


CMD [ "python","preprocess.py" ]
