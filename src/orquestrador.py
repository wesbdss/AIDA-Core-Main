"""
    Creator : Wesley B. D. S. S.
"""

"""
            ----- Descrição -----

    - Cada classe criada é um tipo de processamento dos dados;
    - O processamento deve usar o nome do arquivo criado anteriormente para modularizar os arquivos
    - Os dados devem ser salvo com pickle para leitura posterior;
    - Cada etapa é independente
    -- Decidir qual IA vai usar


Sintaxe dele vai ser

python orquestrador.py PREPROCESSAMENTO PROCESSAMENTO 
"""

import logging
import time
logging.basicConfig(filename='logs/orquestrador'+str(time.time())+'.log', level=logging.DEBUG, format=' %(asctime)s - %(message)s')
import platform
import json
import shutil
from utils.manipularArquivos import ManipularArquivos,FindModules
import os
import docker
import tarfile
import datetime
import random


class Orquestrador:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        logging.debug("{} - {} - {}".format(self.__class__,"Sistema utilizado",platform.system()))

        logging.debug("{} - {} - {}".format(self.__class__,"Path executado",os.getcwd()))

        # 
        #   Criar pastas de saida e entrada por padrão
        # 
        try:
            logging.debug("{} - {} - {}".format(self.__class__,"Criando ","database/output"))
            os.mkdir('database/output')
        except Exception:
            pass
        try:
            logging.debug("{} - {} - {}".format(self.__class__,"Criando ","database/states"))
            os.mkdir('database/states')
        except Exception:
            pass

    def preprocessamento(self, method="AIDA-preprocessamento-1"):

        logging.debug("{} - {} - {}".format(self.__class__,"Iniciando ",method))

        fm = FindModules()
        ma = ManipularArquivos()

        #
        # Compõe a preparação do ambiente para funcionamento do preprocessamento da entrada
        #

        name = "preprocessamento" #Constante, usado para identificação de tipagem dos métodos nos arquivos de configuração

        if method not in fm._list(dir='src/',tipo=name):
            logging.debug("{} - {} - {} - {}".format(self.__class__ ,"ERRO ","Método inexistente ou configuração inválida",method))
            return 0
        #
        # Abre o arquivo de comunicação do processo
        #
        
        with open("src/{}/config.json".format(method), "r") as f:
            configs = json.load(f)
            f.close()


        #
        # Adicionando a base de dados
        #

        logging.debug("{} - {} - {}".format(self.__class__,"Movendo Arquivos Necessários",method))

        fm._movArquivos(lote= configs['arquivos'],dest='src/{}/arquivos'.format(method))
        

        #
        # rodar o docker
        #

        dk = docker.from_env()
        dk.images.build(path="src/{}/".format(method),tag="{}:{}".format(name, configs["version"]))
        try:
            container = dk.containers.run("{}:{}".format(name, configs["version"]),name=configs["name"],remove=False,detach=True)
        except:
            container = dk.containers.get(configs["name"])
            container.remove(force=True)
            container = dk.containers.run("{}:{}".format(name, configs["version"]),name=configs["name"],remove=False,detach=True)

        #
        # Extrair dado do Container
        #

        logging.debug("{} - {} {} - {}".format(self.__class__,"Container Rodando",container.id,method))
        container.wait()
        logging.debug("{} - {} {} - {}".format(self.__class__,"Container Terminado",container.id,method))
        a, b = container.get_archive("output/")

        #
        # Cria pasta do sistema
        #
        try:
            logging.debug("{} - {} -  {} - {}".format(self.__class__,"Criando","database/{}/".format(method),method))
            os.mkdir("database/{}/".format(method))
        except Exception:
            pass

        with open("database/{}/{}.tar".format( method, configs["save"]),"wb") as f:
            for c in a:
                f.write(c)
            f.close()

        #
        # Limpa container desnecessários (CASO DER ERRO, RETIRAR ESSA OPÇâO PARA DEBUG)
        #   WARNING: Se houver containers importantes, não esquecer de remover essa opção

        logging.debug("{} - {} - {} - {}".format(self.__class__,"Warning","Se houver containers importantes não esquecer de remover essa opção",method))
        dk.containers.prune()

        #
        # Extraindo o .zip
        #
        logging.debug("{} - {} - {}".format(self.__class__,"Extraindo zip","database/{}/output".format(method)))
        arquivo = tarfile.open("database/{}/{}.tar".format( method, configs["save"]))
        arquivo.extractall("database/{}".format(method))
        arquivo.close()
        for x in os.listdir("database/{}/output/".format(method)):
            shutil.copy("database/{}/output/{}".format(method, x),"database/{}".format(method))
        ma.deletePasta(dir='database/{}/output'.format(method))
        os.remove("database/{}/{}.tar".format(method,configs["save"]))

        #
        # Limpar a pasta
        #

        ma.deletePasta("src/{}/{}".format(method, "arquivos"))
        return 1

    def processamento(self, method="AIDA-processamento-1", preprocess="AIDA-preprocessamento-1"):

        logging.debug("{} - {} - {}".format(self.__class__,"Iniciando ",method))

        #
        # Compõe a preparação do ambiente para funcionamento do preprocessamento da entrada
        #

        name = "processamento" #Constante, usado para identificação de tipagem dos métodos nos arquivos de configuração

        #
        #   Verifica erros
        #

        fm = FindModules()
        ma = ManipularArquivos()

        if method not in fm._list(dir='src/',tipo=name):
            logging.debug("{} - {} - {} - {}".format(self.__class__ ,"ERRO ","Método inexistente ou configuração inválida (Processamento)",method))
            return 0
        
        if preprocess not in fm._list(dir='src/',tipo="preprocessamento"):
            logging.debug("{} - {} - {} - {}".format(self.__class__ ,"ERRO ","Método inexistente ou configuração inválida (Pre Processamento)",method))
            return 0

        #
        # Abre as configurações
        #

        with open("src/{}/config.json".format(method), "r") as f:  # Etapa corrente configs
            configs = json.load(f)
            f.close()

        with open("src/{}/config.json".format(preprocess), "r") as f:  # Etapa anterior configs
            configs1 = json.load(f)
            f.close()

        #
        # Pegar arquivos do processo anterior
        #

        """
        UPDATE:
            Arrumar pra pegar arquivos dinâmicos, pois as saidas do preprocessamentos são únicas (caso não sejam mais) modificar
        """
        try:
            os.mkdir("src/{}/arquivos".format(method)) 
        except Exception as ex:
            pass
        try:
            for x in configs['arquivos']:
                shutil.copy(x.format(configs1['name'],configs1['output']), "src/{}/arquivos".format(method))
        except Exception as ex:
            logging.debug("{} - {} - {}".format(self.__class__ ,"Arquivos não encontrados",method))
            return 1

        #
        # Executar docker
        #

        dk = docker.from_env()
        dk.images.build(path="src/{}/".format(method),tag="{}:{}".format(name, configs["version"]),)

        try:
            container = dk.containers.run("{}:{}".format(name, configs["version"]),name=configs["name"],remove=False,detach=True)
        except:
            container = dk.containers.get(configs["name"])
            container.remove(force=True)
            container = dk.containers.run("{}:{}".format(name, configs["version"]),name=configs["name"],remove=False,detach=True)
        
        logging.debug("{} - {} {} - {}".format(self.__class__,"Container Rodando",container.id,method))
        container.wait()
        logging.debug("{} - {} {} - {}".format(self.__class__,"Container Terminado",container.id,method))
        a, b = container.get_archive("output/")

        try:
            os.mkdir("database/{}".format(configs["name"]))
        except:
            pass
        with open("database/{}/{}.tar".format(method, configs['output']),"wb") as f:
            for c in a:
                f.write(c)
            f.close()

        #
        # Limpa container desnecessários (CASO DER ERRO, RETIRAR ESSA OPÇâO PARA DEBUG)
        #   WARNING: Se houver containers importantes, não esquecer de remover essa opção

        logging.debug("{} - {} - {} - {}".format(self.__class__,"Warning","Se houver containers importantes não esquecer de remover essa opção",method))
        dk.containers.prune()

        #
        # Extraindo o .zip
        #

        arquivo = tarfile.open("database/{}/{}.tar".format( method, configs['output']))
        arquivo.extractall("database/{}/".format(method))
        arquivo.close()

        
        for x in os.listdir("database/{}/output/".format(method)):
            shutil.copy("database/{}/output/{}".format(method, x),"database/{}".format(method))
        ma.deletePasta('database/{}/output/'.format(method))
        os.remove("database/{}/{}.tar".format(method,configs['output']))

        #
        # Limpar pasta
        #

        ma.deletePasta( "src/{}/{}".format(method, "arquivos"))

        #
        # Gera um log das tecnicas utilizadas
        #

        if os.path.exists('database/output/user.json'):
            maior=0
            with open('database/output/user.json','r') as f:
                arquivo = json.load(f)
                f.close()
                
                for x in arquivo['output']:
                    if x['id'] >= maior:
                        maior = x['id']

        output = {
            "output": [
                {
                    "id": maior+1,
                    "preprocessamento": preprocess,
                    "processamento": method,
                    "data": "{}".format(datetime.datetime.now()),
                    "arquivos": [
                        "database/{}/{}".format( preprocess,configs1['output']),
                        "database/inputs/intents.json",
                        "database/{}".format(method),
                        "database/inputs/fluxo.yaml"
                    ],
                    "version process": configs["version"],
                    "version preprocess": configs1["version"]
                }
            ]
        } 
        logging.debug("{} - {} - {}".format(self.__class__,"Gerando user.json",method))
        if os.path.exists("{}/user.json".format("database/output")):
            with open("{}/user.json".format("database/output"), "r") as f:
                a = json.load(f)
                f.close()
            with open("{}/user.json".format("database/output"), "w") as f:
                output = json.dumps(output["output"])
                output = json.loads(output)
                a["output"].extend(output)
                json.dump(a, f)
                f.close()
        else:
            with open("{}/user.json".format("database/output"), "w") as f:
                json.dump(output, f)
                f.close()
        return 0

    def userCode(self,method="AIDA-usercode",id=1, rand=False,save=False,port=10101):
        """
            UPDATE:
                Adapatação dos caminhos, para os caminhos do config.json
        """
        logging.debug("{} - {} - {}".format(self.__class__,"Iniciando ",method))

        fm = FindModules()
        ma = ManipularArquivos()

        name = "servidor"

        if method not in fm._list(dir='src/',tipo=name):
            logging.debug("{} - {} - {} - {}".format(self.__class__ ,"ERRO ","Método inexistente ou configuração inválida ",method))
            return 0
        
        #
        # Abrindo configurações config.json
        #

        with open('src/{}/config.json'.format(method)) as f:
            conf = json.load(f)
            f.close()

        try:
            with open(conf['userConf'], "r") as f:
                configs = json.load(f)
                f.close()
        except Exception:
            logging.debug("{} - {} - {} - {}".format(self.__class__ ,"ERRO ","Configuração inválida, Rode o Aplicativo Novamente",method))
            return 0

        #
        # Selecionar a Configuração para gerar o Servidor Chatbot
        #

        conf = ""
        if rand:
            for x in configs["output"]:
                conf = x
                break
        else:
            for x in configs["output"]:
                if x["id"] == id:
                    logging.debug("{} - {} - {} - {}".format(self.__class__ ,"Configuração Selecionada",id,method))
                    conf = x
                    break
            if conf == "":
                logging.debug("{} - {} - {}".format(self.__class__ ,"ERRO ","Configuração Não existe",method))
                return 0
        #
        # Buscar arquivos necessários
        #

        try:
            os.mkdir("src/{}/arquivos".format(method))
        except Exception:
            pass

        fm._movArquivos(lote= conf['arquivos'],dest='src/{}/arquivos'.format(method))

        #
        # Mesclar os requeriments
        #

        logging.debug("{} - {} - {}".format(self.__class__ ,"Mesclando Requeriments",method))


        """
        Update:
            Tornar mais dinâmico
        """
        with open('src/{}/requeriments.txt'.format(conf['preprocessamento']),"r") as f:
            p1 = f.read()
            p1 = p1+'\n'
            f.close()
        with open('src/{}/requeriments.txt'.format(conf['processamento']),"r") as f:
            p2 = f.read()
            p1 = p1+p2+'\n'
            f.close()

        with open('src/{}/requeriments.txt'.format(method),"r") as f:
            p2 = f.read()
            p1 = p1+p2
            f.close()
        
        with open('src/{}/requerimentsGen.txt'.format(method),"w") as f:
            p1 = p1.split('\n')
            for x in set(p1):
                f.write(x+'\n')
            f.close()

        
        #
        # Pegar as bibliotecas de cada método
        #
        try:
            os.mkdir("src/{}/libs".format(method))
        except Exception:
            pass

        try:
            shutil.copy('src/{}/preprocess.py'.format(conf['preprocessamento'],x),'src/{}/libs'.format(method))
            shutil.copy('src/{}/process.py'.format(conf['processamento'],x),'src/{}/libs'.format(method))
            shutil.copy('utils/componenteServer.py','src/{}/libs'.format(method))
            shutil.copy('utils/AIDA-fluxo','src/{}/libs'.format(method))
        except Exception:
            logging.debug("{} - {} - {}".format(self.__class__ ,"Não Há Requerimentos",method))


        

        #
        # Criar a maquina docker pra rodar - salvar a máquina
        #

        dk = docker.from_env()
        img = dk.images.build(path="src/{}/".format(method),tag='server:{}'.format(conf['id']))
        
        try:
            container = dk.containers.run('server:{}'.format(conf['id']),ports={'10101/tcp':port},name=method,remove=False,detach=True)
        except Exception as ex:
            container = dk.containers.get(method)
            container.remove(force=True)
            container = dk.containers.run('server:{}'.format(conf['id']),ports={'10101/tcp':port},name=method.format(method),remove=False,detach=True)
        
        logging.debug("{} - {} - {}".format(self.__class__ ,"Servidor Rodando localhost:10101",method))


        #
        # Limpa as imagens
        #

        logging.debug("{} - {} - {} - {}".format(self.__class__,"Warning","Se houver containers importantes não esquecer de remover essa opção",method))
        dk.containers.prune()


        #
        # Salvar estado dos dados
        #

        if save:
            try:
                os.mkdir('database/states/{}'.format(conf['id']))
            except Exception:
                pass
            fm._movArquivos(['src/{}/libs'.format(method)],dest='database/states/{}/libs'.format(conf['id']))
            fm._movArquivos(['src/{}/arquivos'.format(method)],dest='database/states/{}/arquivos'.format(conf['id']))
            shutil.copy('src/{}/server.py'.format(method),'database/states/{}/'.format(conf['id']))
            shutil.copy('src/{}/requerimentsGen.txt'.format(method),'database/states/{}/'.format(conf['id']))
            shutil.copy('src/{}/Dockerfile'.format(method),'database/states/{}/'.format(conf['id']))
            with open("database/states/{}/config.json".format(conf['id']),"w") as f:
                f.write(json.dumps(conf))
                f.close()

        #
        # Limpar os dados
        #
        ma.deletePasta('src/{}/libs'.format(method))
        ma.deletePasta('src/{}/arquivos'.format(method))
        os.remove('src/{}/requerimentsGen.txt'.format(method))
        return 1