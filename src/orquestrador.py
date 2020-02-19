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

class Orquestrador:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.__class__,">> Sistema Utilizado: ", platform.system())
        path = os.getcwd()
        print (self.__class__,"O programa está sendo executado em -->  %s" % path)
        
    
    def preprocessamento(self,method='metodo1'):
        name = 'preprocessamento'
        dirbase = 'src/'
        if method not in os.listdir(dirbase):
            print(self.__class__,"ERR: Método inexistente")
            return 1
        
        with open('{}/{}/config.json'.format(dirbase,method),'r') as f:
            configs = json.load(f)
            f.close()
        

        #
        #   Caminho dos dados a serem utilizados
        #

        dataFile = configs['input']

        #
        # mover arquivos do util para pasta com docker
        #

        diretory = 'utils'
        ar = os.listdir(path=diretory)
        ar = [w for w in ar if w not in ['__pycache__']]
        try:
            os.mkdir('{}/{}/preprocess/{}/'.format(dirbase,method,diretory))
        except:
            pass
        for x in ar:
            shutil.copy('{}/{}'.format(diretory,x),'{}/{}/preprocess/{}/'.format(dirbase,method,diretory))
        
        #
        # Adicionando a base de dados
        #

        """
        UPDATE:

        implementar modo, multi intents
        """
        try:
            os.mkdir('{}/{}/preprocess/database/'.format(dirbase,method))
        except:
            pass
        shutil.copy('{}'.format(configs['input']),'{}/{}/preprocess/database/'.format(dirbase,method))

        print(self.__class__,"Movendo Arquivos necessários")

        #
        # rodar o docker
        #

        dk = docker.from_env()
        dk.images.build(path ='{}/{}/preprocess/'.format(dirbase,method),tag="{}:{}".format(name,configs['version']))
        try:
            container = dk.containers.run("{}:{}".format(name,configs['version']),name=configs['name'],remove=False,detach=True)
        except:
            container = dk.containers.get(configs['name'])
            container.remove(force=True)
            container = dk.containers.run("{}:{}".format(name,configs['version']),name=configs['name'],remove=False,detach=True)
            
        #
        # Extrair dado do Container
        #

        print(self.__class__,"Container {} Rodando ...".format(container.id))
        container.wait()
        print(self.__class__,"Container {} Terminou".format(container.id))
        a,b = container.get_archive('output/')

        try:
            os.mkdir('{}'.format(configs['output preprocess']))
            os.mkdir('{}/{}'.format(configs['output preprocess'],method))
        except Exception:
            pass

        with open('{}/{}/{}.tar'.format(configs['output preprocess'],method,configs['output preprocess name']),'wb') as f:
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

        arquivo = tarfile.open('{}/{}/{}.tar'.format(configs['output preprocess'],method,configs['output preprocess name']))
        arquivo.extractall('{}/{}'.format(configs['output preprocess'],method))
        arquivo.close()
        for x in os.listdir('{}/{}/output/'.format(configs['output preprocess'],method)):
            shutil.copy('{}/{}/output/{}'.format(configs['output preprocess'],method,x),'{}/{}'.format(configs['output preprocess'],method))
            os.remove('{}/{}/output/{}'.format(configs['output preprocess'],method,x))
        os.rmdir('{}/{}/output'.format(configs['output preprocess'],method))
        os.remove('{}/{}/{}.tar'.format(configs['output preprocess'],method,configs['output preprocess name']))

        #
        # Limpar a pasta
        #

        temp = os.listdir('{}/{}/preprocess/{}'.format(dirbase,method,'utils'))
        for x in temp:
            os.remove('{}/{}/preprocess/{}/{}'.format(dirbase,method,'utils',x))
        os.rmdir('{}/{}/preprocess/{}'.format(dirbase,method,'utils'))
        temp = os.listdir('{}/{}/preprocess/{}'.format(dirbase,method,'database'))
        for x in temp:
            os.remove('{}/{}/preprocess/{}/{}'.format(dirbase,method,'database',x))
        os.rmdir('{}/{}/preprocess/{}'.format(dirbase,method,'database'))

        return 0

    def processamento(self,method='metodo1',preprocess= 'metodo1'):
        name='processamento'
        dirbase = 'src'

        #
        #   Verifica erros
        #

        if method not in os.listdir(dirbase):
            print(self.__class__,"ERR: Método inexistente")
            return 1

        #
        # Abre as configurações
        #

        with open('{}/{}/config.json'.format(dirbase,method),'r') as f: #Etapa corrente configs
            configs = json.load(f)
            f.close()

        with open('{}/{}/config.json'.format(dirbase,preprocess),'r') as f: #Etapa anterior configs
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
            os.mkdir('{}/{}/process-intents/database'.format(dirbase,method))
        except Exception as ex:
            pass
        try: 
            shutil.copy('{}/{}/data.pickle'.format(configs1['output preprocess'],preprocess),'{}/{}/process-intents/database/'.format(dirbase,method))
        except Exception as ex:
            print(self.__class__,"Arquivo de dados pre processados não encontrados ",ex)
            return 1
        
        #
        # Executar docker
        #
        
        dk = docker.from_env()
        dk.images.build(path ='{}/{}/process-intents/'.format(dirbase,method),tag="{}:{}".format(name,configs['version']))

        try:
            container = dk.containers.run("{}:{}".format(name,configs['version']),name=configs['name'],remove=False,detach=True)
        except:
            container = dk.containers.get(configs['name'])
            container.remove(force=True)
            container = dk.containers.run("{}:{}".format(name,configs['version']),name=configs['name'],remove=False,detach=True)
        
        print(self.__class__,"Container {} Rodando ...".format(container.id))
        container.wait()
        print(self.__class__,"Container {} Terminou".format(container.id))
        a,b = container.get_archive('output/')

        try:
            os.mkdir('{}'.format(configs['output process']))
            os.mkdir('{}/{}'.format(configs['output process'],method))
        except:
            pass
        print(a)
        with open('{}/{}/{}.tar'.format(configs['output process'],method,configs['output process name']),'wb') as f:
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

        arquivo = tarfile.open('{}/{}/{}.tar'.format(configs['output process'],method,configs1['output process name']))
        arquivo.extractall('{}/{}/'.format(configs['output process'],method))
        arquivo.close()
        for x in os.listdir('{}/{}/output/'.format(configs['output process'],method)):
            shutil.copy('{}/{}/output/{}'.format(configs['output process'],method,x),'{}/{}'.format(configs['output process'],method))
            os.remove('{}/{}/output/{}'.format(configs['output process'],method,x))
        
        os.rmdir('{}/{}/output'.format(configs['output process'],method))
        os.remove('{}/{}/{}.tar'.format(configs['output process'],method,configs['output process name']))

        #
        # Limpar pasta
        #

        for x in os.listdir('{}/{}/process-intents/{}'.format(dirbase,method,'database')):
            os.remove('{}/{}/process-intents/{}/{}'.format(dirbase,method,'database',x))
        os.rmdir('{}/{}/process-intents/{}'.format(dirbase,method,'database'))

        #
        # Gera um log das tecnicas utilizadas
        #
        output = {
            "preprocessamento":preprocess,
            "processamento":method,
            "data": '{}'.format(datetime.datetime.now()),
            "dado processado": '{}/{}/data.pickle'.format(configs1['output preprocess'],preprocess),
            "dado input": '{}'.format(configs1['input']),
            "modelo": '{}/{}'.format(configs['output process'],method),
            "version":configs['version']
        }
        print(self.__class__,"Gerando user.json ")
        with open('{}/user.json'.format('database/output'),'w') as f:
            json.dump(output,f)
            f.close()
        return 0

    def userCode(self, baseUser='user.json'):
        with open('database/output/'+baseUser) as f:
            configs = json.load(f)
            f.close()

        

        #
        # Mesclar os requeriments
        #

        #
        # Pegar as bibliotecas de cada método
        #

        #
        # Criar a maquina docker pra rodar - salvar a máquina
        #

        #
        # Limpar os dados
        #