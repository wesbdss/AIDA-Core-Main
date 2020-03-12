import os
import json
import re
import logging
import shutil

class FindModules:

    def __init__(self):
        pass

    def _list(self,dir='',ignore=[],tipo=''):
        
        #
        # Lista pastas Válidas (Representando os métodos disponiveis)
        #
        logging.debug("{} - {} - Parameters - {} - {}".format(self.__class__,"_list",ignore,tipo))


        ignore.append('__pycache__')
        arquivos = os.listdir(dir)
        arquivos = [x for x in arquivos if x not in ignore]
        lixo = []
        for x in arquivos:
            lixo.append(re.search('[a-zA-Z\_\-\+]+\.[a-zA-Z]+',x))
            lixo.append(re.search('[a-zA-Z\_\-\+]+\_teste',x))
        lixo = set(lixo)
        lixo.remove(None)
        for x in lixo:
            arquivos.remove(x.group())

        if tipo != '':
            arquivos = [x for x in arquivos if self._type(name=x,dir=dir) == tipo]
        return arquivos

    def _type(self,name='',dir=''):
        #
        # Verifica a tipagem do módulo
        #
        logging.debug("{} - {} - Parameters - {} - {}".format(self.__class__,"_type",name,dir))

        with open('{}/{}/config.json'.format(dir,name),'r') as f:
            confs = json.load(f)
            f.close()
        return confs['type']

    def _movArquivos(self,lote=[],dest=''):
        #
        # Copia um lote arquivos para uma pasta, ainda pode criar apenas mais uma pasta que não existe
        #
        logging.debug("{} - {} - Parameters - {} - {}".format(self.__class__,"_movArquivos",lote,dest))
        try:
            os.mkdir(dest)
        except Exception:
            pass
        for x in lote:
            try:
                shutil.copy(x,dest)
            except Exception:
                for y in os.listdir(x):
                    shutil.copy("{}/{}".format(x,y),dest)



class ManipularArquivos:
    def __init__(self):
        pass
    
    def deletePasta(self,dir=''):
        #
        # Deleta a pasta e seus arquivos
        #

        logging.debug("{} - {} - Parameters - {}".format(self.__class__,"deletePasta",dir))

        if dir == '':
            return 1
        try:
            try:
                for x in os.listdir(dir):
                    os.remove("{}/{}".format(dir,x))
                os.rmdir(dir)
            except Exception:
                os.rmdir(dir)
                
        except Exception:
            logging.debug("{} - {} - Parameters - {} - {}".format(self.__class__,"Erro","Caminho da pasta não existe",dir))


class Intents():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def readJson(self='',dir=''): # lê o arquivo json inteiro
        logging.debug("{} - {} - Parameters - {} - {}".format(self.__class__,"readJson",dir))

        if dir == '':
            dir = "./data/intents.json"

        if not os.path.exists(dir): 
            print("O diretório "+dir+ " não existe ")
            print(os.listdir())
        else:
            with open(dir) as data:
                dados = json.load(data)
            return dados
        
    def writeIntent (self, tag ='', value = '',dir= ''): #escreve uma tag e um valor no arquivo
        logging.debug("{} - {} - Parameters - {} - {} - {}".format(self.__class__,"writeIntent",tag,value,dir))

        if dir == '':
            dir = "./data/intents.json"
        if tag == '' or value == '':
            print("Um dos valores estão em Branco")
            return ''

        else: 
            with open(dir,encoding='utf-8') as data:
                dados = json.load(data)
            find = False
            for x in range(0,len(dados['intents'])):
                if tag in dados['intents'][x]['tag']:
                    if not value in dados['intents'][x]['patterns']:
                        dados['intents'][x]['patterns'].append(value)
                    find = True
                    break
            if not find:
                dados['intents'].append({'tag': tag,'patterns': [value],'responses':['']})
            with open(dir,'w',encoding='utf-8') as data:
                json.dump(dados,data,indent= 3,ensure_ascii=False)
            return 'OK'
        
    def readIntent (self,tag ='',dir=''): #encontra a tag em um arquivo json
        logging.debug("{} - {} - Parameters - {} - {}".format(self.__class__,"readIntent",tag,dir))

        if dir == '':
            dir = "./data/intents.json"
        if tag == '':
            print("Tag vazia")
            return ''
        dados = ''
        with open(dir,encoding='utf-8') as data:
            dados = json.load(data)
        
        for x in range(0,len(dados['intents'])):
            if dados['intents'][x]['tag'] == tag:
                return dados['intents'][x]
        return ''