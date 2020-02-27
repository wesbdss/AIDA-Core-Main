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

    def preprocessamento(self, method="AIDA-preprocessamento-1"):
        ignore = ['coisasParaApagar_teste'] # pastas testes, para ignorar
        name = "preprocessamento"
        dirbase = "src/"
        output= 'data'
        fm = FindModules()
        ma = ManipularArquivos()
        if method not in fm._list(dir='src/',ignore=ignore,tipo=name):
            print(self.__class__, "ERR: Método inexistente")
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

    def processamento(self, method="metodo1", preprocess="metodo1"):
        name = "processamento"
        dirbase = "src"

        #
        #   Verifica erros
        #

        if method not in os.listdir(dirbase):
            print(self.__class__, "ERR: Método inexistente")
            return 1

        #
        # Abre as configurações
        #

        with open(
            "{}/{}/config.json".format(dirbase, method), "r"
        ) as f:  # Etapa corrente configs
            configs = json.load(f)
            f.close()

        with open(
            "{}/{}/config.json".format(dirbase, preprocess), "r"
        ) as f:  # Etapa anterior configs
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
            os.mkdir("{}/{}/process-intents/database".format(dirbase, method))
        except Exception as ex:
            pass
        try:
            shutil.copy("{}/{}/data.pickle".format(configs1["output preprocess"], preprocess), "{}/{}/process-intents/database/".format(dirbase, method))
        except Exception as ex:
            print(
                self.__class__, "Arquivo de dados pre processados não encontrados ", ex
            )
            return 1

        #
        # Executar docker
        #

        dk = docker.from_env()
        dk.images.build(
            path="{}/{}/process-intents/".format(dirbase, method),
            tag="{}:{}".format(name, configs["version"]),
        )

        try:
            container = dk.containers.run(
                "{}:{}".format(name, configs["version"]),
                name=configs["name"],
                remove=False,
                detach=True,
            )
        except:
            container = dk.containers.get(configs["name"])
            container.remove(force=True)
            container = dk.containers.run(
                "{}:{}".format(name, configs["version"]),
                name=configs["name"],
                remove=False,
                detach=True,
            )
        print(self.__class__, "Container {} Rodando ...".format(container.id))
        container.wait()
        print(self.__class__, "Container {} Terminou".format(container.id))
        a, b = container.get_archive("output/")

        try:
            os.mkdir("{}".format(configs["output process"]))
            os.mkdir("{}/{}".format(configs["output process"], method))
        except:
            pass
        print(a)
        with open(
            "{}/{}/{}.tar".format(
                configs["output process"], method, configs["output process name"]
            ),
            "wb",
        ) as f:
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

        arquivo = tarfile.open(
            "{}/{}/{}.tar".format(
                configs["output process"], method, configs1["output process name"]
            )
        )
        arquivo.extractall("{}/{}/".format(configs["output process"], method))
        arquivo.close()

        
        for x in os.listdir("{}/{}/output/".format(configs["output process"], method)):
            shutil.copy(
                "{}/{}/output/{}".format(configs["output process"], method, x),
                "{}/{}".format(configs["output process"], method),
            )
            os.remove("{}/{}/output/{}".format(configs["output process"], method, x))

        os.rmdir("{}/{}/output".format(configs["output process"], method))
        os.remove(
            "{}/{}/{}.tar".format(
                configs["output process"], method, configs["output process name"]
            )
        )

        #
        # Limpar pasta
        #

        self.__manipula.deletePasta( "{}/{}/process-intents/{}".format(dirbase, method, "database"))

        #
        # Gera um log das tecnicas utilizadas
        #

        output = {
            "output": [
                {
                    "id": (random.randrange(0, 999999999)),
                    "preprocessamento": preprocess,
                    "processamento": method,
                    "data": "{}".format(datetime.datetime.now()),
                    "arquivos": [
                        "{}/{}/data.pickle".format(
                            configs1["output preprocess"], preprocess
                        ),
                        "{}".format(configs1["input"]),
                        "{}/{}".format(configs["output process"], method),
                    ],
                    "version": configs["version"],
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

    def userCode(self, baseUser="database/output/user.json", id=123, rand=False,save=False):
        
        try:
            with open(baseUser, "r") as f:
                configs = json.load(f)
        except Exception:
            print(
                self.__class__, "ERRO: Não há configuração, rode o aplicativo novamente"
            )
            return 1

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
                return 1
        name = "Servidor"
        #
        # Buscar arquivos necessários
        #
        """
            Caso houver mesclagem de métodos tem que melhorar essa parte
        """
        try:
            with open("src/{}/config.json".format(conf['preprocessamento']), "r") as f:
                configs = json.load(f)
        except Exception:
            print(
                self.__class__, "ERRO: Não há configuração, rode o aplicativo novamente"
            )
            return 1

        try:
            os.mkdir("src/userCode/arquivos")
        except Exception:
            pass
        for x in conf['arquivos']:
            try:
                shutil.copy(x,'src/userCode/arquivos')
            except Exception as ex: #pega subarquivos  UMA PROFUNDIDADE APENAS
                for y in os.listdir(x):
                    shutil.copy('{}/{}'.format(x,y),'{}'.format('src/userCode/arquivos'))

        #
        # Mesclar os requeriments
        #
        print(self.__class__,"Mesclando Requeriments")

        """
        Update:
            Tornar mais dinâmico
        """
        with open('src/{}/preprocess/requeriments.txt'.format(conf['preprocessamento']),"r") as f:
            p1 = f.read()
            p1 = p1+'\n'
            f.close()
        with open('src/{}/process-intents/requeriments.txt'.format(conf['processamento']),"r") as f:
            p2 = f.read()
            p1 = p1+p2+'\n'
            f.close()

        with open('src/userCode/requeriments.txt',"r") as f:
            p2 = f.read()
            p1 = p1+p2
            f.close()
        
        with open('src/userCode/requerimentsGen.txt',"w") as f:
            p1 = p1.split('\n')
            for x in set(p1):
                f.write(x+'\n')
            f.close()
        #
        # Pegar as bibliotecas de cada método
        #
        try:
            os.mkdir("src/userCode/libs")
        except Exception:
            pass

        for x in configs['requerimentos'].keys():
            try:
                shutil.copy('src/{}/{}/preprocess.py'.format(configs['name'],x),'src/userCode/libs')
            except:
                pass
            try:
                shutil.copy('src/{}/{}/process.py'.format(configs['name'],x),'src/userCode/libs')
            except:
                pass

        #
        # Criar a maquina docker pra rodar - salvar a máquina
        #
        dk = docker.from_env()
        img = dk.images.build(path="src/userCode/",tag='server:{}'.format(conf['version']))
 
        print('Preparando maquina Docker')
        try:
            container = dk.containers.run('server:{}'.format(conf['version']),ports={'10101/tcp':10101},name='Servidor',remove=False,detach=True)
        except Exception as ex:
            container = dk.containers.get('Servidor')
            container.remove(force=True)
            container = dk.containers.run('server:{}'.format(conf['version']),ports={'10101/tcp':10101},name='Servidor',remove=False,detach=True)
        print(self.__class__, "Container {} Rodando ...".format(container.id))

        #
        # Limpa as imagens
        #

        
        print("Servidor rodando !! 0.0.0.0:10101")

        dk.containers.prune()

        if save:
            img.save()
        #
        # Limpar os dados
        #
        self.__manipula.deletePasta('src/userCode/libs')
        self.__manipula.deletePasta('src/userCode/arquivos')

        
        
