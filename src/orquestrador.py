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
        print(self.__class__, ">> Sistema Utilizado: ", platform.system())
        path = os.getcwd()
        print(self.__class__, "O programa está sendo executado em -->  %s" % path)
        """
            Criar pastas de saida e entrada por padrão
        """
        try:
            os.mkdir('database/output')
        except Exception:
            pass
        try:
            os.mkdir('database/states')
        except Exception:
            pass

    def preprocessamento(self, method="AIDA-preprocessamento-1"):

        #
        # Compõe a preparação do ambiente para funcionamento do preprocessamento da entrada
        #

        name = "preprocessamento"
        dirbase = "src"
        output= 'data'

        fm = FindModules()
        ma = ManipularArquivos()

        if method not in fm._list(dir='src/',tipo=name):
            print(self.__class__, "ERR: Método inexistente ou configuração inválida")
            return 0
        #
        # Abre o arquivo de comunicação do processo
        #
        
        with open("{}/{}/config.json".format(dirbase, method), "r") as f:
            configs = json.load(f)
            f.close()

        #
        #   Caminho dos dados a serem utilizados
        #  

        if configs['type'] != name:
            print(self.__class__,"Esse método não é do tipo preprocessamento")
            return 0

        #
        # Adicionando a base de dados
        #

        fm._movArquivos(lote= configs['arquivos'],dest='{}/{}/arquivos'.format(dirbase,method))
        print(self.__class__, "Movendo Arquivos necessários")

        #
        # rodar o docker
        #

        dk = docker.from_env()
        dk.images.build(path="{}/{}/".format(dirbase, method),tag="{}:{}".format(name, configs["version"]))
        try:
            container = dk.containers.run("{}:{}".format(name, configs["version"]),name=configs["name"],remove=False,detach=True)
        except:
            container = dk.containers.get(configs["name"])
            container.remove(force=True)
            container = dk.containers.run("{}:{}".format(name, configs["version"]),name=configs["name"],remove=False,detach=True)

        #
        # Extrair dado do Container
        #

        print(self.__class__, "Container {} Rodando ...".format(container.id))
        container.wait()
        print(self.__class__, "Container {} Terminou".format(container.id))
        a, b = container.get_archive("output/")

        #
        # Cria pasta do sistema
        #
        try:
            os.mkdir("database/{}/".format(method))
        except Exception:
            pass

        with open("database/{}/{}.tar".format( method, output),"wb") as f:
            for c in a:
                f.write(c)
            f.close()

        #
        # Limpa container desnecessários (CASO DER ERRO, RETIRAR ESSA OPÇâO PARA DEBUG)
        #   WARNING: Se houver containers importantes, não esquecer de remover essa opção

        print("Warning: Os containers não utilizados serão apagados!")
        dk.containers.prune()

        #
        # Extraindo o .zip
        #

        arquivo = tarfile.open("database/{}/{}.tar".format( method, output))
        arquivo.extractall("database/{}".format(method))
        arquivo.close()
        for x in os.listdir("database/{}/output/".format(method)):
            shutil.copy("database/{}/output/{}".format(method, x),"database/{}".format(method))
        ma.deletePasta(dir='database/{}/output'.format(method))
        os.remove("database/{}/{}.tar".format(method,output))

        #
        # Limpar a pasta
        #

        ma.deletePasta("{}/{}/{}".format(dirbase, method, "arquivos"))
        return 1

    def processamento(self, method="AIDA-processamento-1", preprocess="AIDA-preprocessamento-1"):

        #
        # Compõe a preparação do ambiente para funcionamento do preprocessamento da entrada
        #

        name = "processamento"
        dirbase = "src"
        output= "data"

        #
        #   Verifica erros
        #

        fm = FindModules()
        ma = ManipularArquivos()

        if method not in fm._list(dir='src/',tipo=name):
            print(self.__class__, "ERR: Método inexistente ou configuração inválida")
            return 0
        
        if preprocess not in fm._list(dir='src/',tipo="preprocessamento"):
            print(self.__class__, "ERR: Método inexistente ou configuração inválida")
            return 0

        #
        # Abre as configurações
        #

        with open("{}/{}/config.json".format(dirbase, method), "r") as f:  # Etapa corrente configs
            configs = json.load(f)
            f.close()

        with open("{}/{}/config.json".format(dirbase, preprocess), "r") as f:  # Etapa anterior configs
            configs1 = json.load(f)
            f.close()

        #
        # Pegar arquivos do processo anterior
        #

        """
        UPDATE:
            Arrumar pra pegar arquivos dinâmicos
        """
        try:
            os.mkdir("{}/{}/arquivos".format(dirbase, method))
        except Exception as ex:
            pass
        try:
            for x in configs['arquivos']:
                shutil.copy(x.format(configs1['name'],configs1['save']), "{}/{}/arquivos".format(dirbase, method))
        except Exception as ex:
            print(self.__class__, "Arquivo de dados pre processados não encontrados ", ex)
            return 1

        #
        # Executar docker
        #

        dk = docker.from_env()
        dk.images.build(path="{}/{}/".format(dirbase, method),tag="{}:{}".format(name, configs["version"]),)

        try:
            container = dk.containers.run("{}:{}".format(name, configs["version"]),name=configs["name"],remove=False,detach=True)
        except:
            container = dk.containers.get(configs["name"])
            container.remove(force=True)
            container = dk.containers.run("{}:{}".format(name, configs["version"]),name=configs["name"],remove=False,detach=True)
        
        print(self.__class__, "Container {} Rodando ...".format(container.id))
        container.wait()
        print(self.__class__, "Container {} Terminou".format(container.id))
        a, b = container.get_archive("output/")

        try:
            os.mkdir("database/{}".format(configs["name"]))
        except:
            pass
        with open("database/{}/{}.tar".format(method, output),"wb") as f:
            for c in a:
                f.write(c)
            f.close()

        #
        # Limpa container desnecessários (CASO DER ERRO, RETIRAR ESSA OPÇâO PARA DEBUG)
        #   WARNING: Se houver containers importantes, não esquecer de remover essa opção

        print("Warning: Os containers não utilizados serão apagados!")
        dk.containers.prune()

        #
        # Extraindo o .zip
        #

        arquivo = tarfile.open("database/{}/{}.tar".format( method, output))
        arquivo.extractall("database/{}/".format(method))
        arquivo.close()

        
        for x in os.listdir("database/{}/output/".format(method)):
            shutil.copy("database/{}/output/{}".format(method, x),"database/{}".format(method))
        ma.deletePasta('database/{}/output/'.format(method))
        os.remove("database/{}/{}.tar".format(method,output))

        #
        # Limpar pasta
        #

        ma.deletePasta( "{}/{}/{}".format(dirbase, method, "arquivos"))

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
                        "database/{}/{}".format( preprocess,configs1['save']),
                        "database/inputs/intents.json",
                        "database/{}".format(method),
                    ],
                    "version process": configs["version"],
                    "version preprocess": configs1["version"]
                }
            ]
        } 
        print(self.__class__, "Gerando user.json ")
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

    def userCode(self, baseUser="database/output/user.json",method="AIDA-usercode",id=1, rand=False,save=False,port=10101):
        fm = FindModules()
        name = "servidor"
        ma = ManipularArquivos()

        if method not in fm._list(dir='src/',tipo=name):
            print(self.__class__, "ERR: Método inexistente ou configuração inválida")
            return 0

        try:
            with open(baseUser, "r") as f:
                configs = json.load(f)
                f.close()
        except Exception:
            print(self.__class__, "ERRO: Não há configuração, rode o aplicativo processamento e o preprocessamento")
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
                    print(self.__class__, "Configuração selecionada: {}".format(id))
                    conf = x
                    break
            if conf == "":
                print(self.__class__, "Configuração {} não existe")
                return 0
        #
        # Buscar arquivos necessários
        #

        try:
            os.mkdir("src/{}/arquivos".format(method))
        except Exception:
            pass
        for x in conf['arquivos']:
            try:
                shutil.copy(x,'src/{}/arquivos'.format(method))
            except Exception as ex: #pega subarquivos  UMA PROFUNDIDADE APENAS
                for y in os.listdir(x):
                    shutil.copy('{}/{}'.format(x,y),'{}'.format('src/{}/arquivos'.format(method)))

        #
        # Mesclar os requeriments
        #

        print(self.__class__,"Mesclando Requeriments")

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
        except Exception:
            print("Não há requeriments")

        

        #
        # Criar a maquina docker pra rodar - salvar a máquina
        #
        dk = docker.from_env()
        img = dk.images.build(path="src/{}/".format(method),tag='server:{}'.format(conf['id']))
        
        print(self.__class__,'Preparando maquina Docker')
        try:
            container = dk.containers.run('server:{}'.format(conf['id']),ports={'10101/tcp':port},name=method,remove=False,detach=True)
        except Exception as ex:
            container = dk.containers.get(method)
            container.remove(force=True)
            container = dk.containers.run('server:{}'.format(conf['id']),ports={'10101/tcp':port},name=method.format(method),remove=False,detach=True)
        print(self.__class__, "Container {} Rodando ...".format(container.id))

        #
        # Limpa as imagens
        #

        
        print(self.__class__,"Servidor Rodando 0.0.0.0:{}".format(port))

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