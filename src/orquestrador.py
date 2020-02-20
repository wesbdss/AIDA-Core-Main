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

    def preprocessamento(self, method="metodo1"):
        name = "preprocessamento"
        dirbase = "src/"
        if method not in os.listdir(dirbase):
            print(self.__class__, "ERR: Método inexistente")
            return 1

        with open("{}/{}/config.json".format(dirbase, method), "r") as f:
            configs = json.load(f)
            f.close()

        #
        #   Caminho dos dados a serem utilizados
        #

        dataFile = configs["input"]

        #
        # mover arquivos do util para pasta com docker
        #

        diretory = "utils"
        ar = os.listdir(path=diretory)
        ar = [w for w in ar if w not in ["__pycache__"]]
        try:
            os.mkdir("{}/{}/preprocess/{}/".format(dirbase, method, diretory))
        except:
            pass
        for x in ar:
            shutil.copy(
                "{}/{}".format(diretory, x),
                "{}/{}/preprocess/{}/".format(dirbase, method, diretory),
            )

        #
        # Adicionando a base de dados
        #

        """
        UPDATE:

        implementar modo, multi intents
        """
        try:
            os.mkdir("{}/{}/preprocess/database/".format(dirbase, method))
        except:
            pass
        shutil.copy(
            "{}".format(configs["input"]),
            "{}/{}/preprocess/database/".format(dirbase, method),
        )

        print(self.__class__, "Movendo Arquivos necessários")

        #
        # rodar o docker
        #

        dk = docker.from_env()
        dk.images.build(
            path="{}/{}/preprocess/".format(dirbase, method),
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

        #
        # Extrair dado do Container
        #

        print(self.__class__, "Container {} Rodando ...".format(container.id))
        container.wait()
        print(self.__class__, "Container {} Terminou".format(container.id))
        a, b = container.get_archive("output/")

        try:
            os.mkdir("{}".format(configs["output preprocess"]))
            os.mkdir("{}/{}".format(configs["output preprocess"], method))
        except Exception:
            pass

        with open(
            "{}/{}/{}.tar".format(
                configs["output preprocess"], method, configs["output preprocess name"]
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
                configs["output preprocess"], method, configs["output preprocess name"]
            )
        )
        arquivo.extractall("{}/{}".format(configs["output preprocess"], method))
        arquivo.close()
        for x in os.listdir(
            "{}/{}/output/".format(configs["output preprocess"], method)
        ):
            shutil.copy(
                "{}/{}/output/{}".format(configs["output preprocess"], method, x),
                "{}/{}".format(configs["output preprocess"], method),
            )
            os.remove("{}/{}/output/{}".format(configs["output preprocess"], method, x))
        os.rmdir("{}/{}/output".format(configs["output preprocess"], method))
        os.remove(
            "{}/{}/{}.tar".format(
                configs["output preprocess"], method, configs["output preprocess name"]
            )
        )

        #
        # Limpar a pasta
        #

        temp = os.listdir("{}/{}/preprocess/{}".format(dirbase, method, "utils"))
        for x in temp:
            os.remove("{}/{}/preprocess/{}/{}".format(dirbase, method, "utils", x))
        os.rmdir("{}/{}/preprocess/{}".format(dirbase, method, "utils"))
        temp = os.listdir("{}/{}/preprocess/{}".format(dirbase, method, "database"))
        for x in temp:
            os.remove("{}/{}/preprocess/{}/{}".format(dirbase, method, "database", x))
        os.rmdir("{}/{}/preprocess/{}".format(dirbase, method, "database"))

        return 0

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
            shutil.copy(
                "{}/{}/data.pickle".format(configs1["output preprocess"], preprocess),
                "{}/{}/process-intents/database/".format(dirbase, method),
            )
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

        for x in os.listdir(
            "{}/{}/process-intents/{}".format(dirbase, method, "database")
        ):
            os.remove(
                "{}/{}/process-intents/{}/{}".format(dirbase, method, "database", x)
            )
        os.rmdir("{}/{}/process-intents/{}".format(dirbase, method, "database"))

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

    def userCode(self, baseUser="database/output/user.json", id=123, rand=False):
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

        if rand:
            for x in configs["output"]:
                conf = x
                break
        else:
            conf = ""
            for x in configs["output"]:
                if x["id"] == id:
                    print(self.__class__, "Configuração selecionada: {}".format(id))
                    conf = x
                    break
            if conf == "":
                print(self.__class__, "Configuração {} não existe")
                return 1

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

        with open('src/{}/preprocess/requeriments.txt'.format(conf['preprocessamento']),"r") as f:
            p1 = f.read()
            p1 = p1+'\n'
            f.close()
        with open('src/{}/preprocess/requeriments.txt'.format(conf['processamento']),"r") as f:
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

        print(configs['requerimentos'].keys())
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

        #
        # Limpar os dados
        #
