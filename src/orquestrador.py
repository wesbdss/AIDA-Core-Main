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
import shutil
import os
import docker
from utils.findImports import FindImports
import tarfile

ver = 'v1'


class Orquestrador:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.__class__,">> Sistema Utilizado: ", platform.system())
        path = os.getcwd()
        print (self.__class__,"O programa está sendo executado em -->  %s" % path)
        self.imp = FindImports()
        
    
    def preprocessamento(self,method='method1',dataFile=[]):
        name = 'preprocess'

        #
        #   Caminho dos dados a serem utilizados
        #

        if dataFile == []:
            dataFile = ['intents.json']

        #
        # mover arquivos do util para os dockers
        #

        diretory = 'utils'
        ar = os.listdir(path=diretory)
        ar = [w for w in ar if w not in ['__pycache__']]
        try:
            os.mkdir('src/1-preprocess/{}/{}/'.format(method,diretory))
        except:
            pass
        for x in ar:
            shutil.copy('{}/{}'.format(diretory,x),'src/1-preprocess/{}/{}/'.format(method,diretory))
        
        #
        # Adicionando a base de dados
        #

        try:
            local = self.imp.findDiretory(arq=dataFile,local='database')
        except Exception:
            print(self.__class__,"ERR >> Arquivo não encontrado")
            return 1
        diretorybase = local[0]['dir']
        datab = [x['dir'] for x in local]
        try:
            os.mkdir('src/1-preprocess/{}/database/'.format(method))
        except:
            pass
        for x in datab:
            shutil.copy('{}'.format(x),'src/1-preprocess/{}/database/'.format(method))

        print(self.__class__,"Movendo Arquivos necessários")

        #
        # rodar o docker
        #

        dk = docker.from_env()
        dk.images.build(path ='src/1-preprocess/{}/'.format(method),tag="{}:{}".format(name,ver))
        try:
            container = dk.containers.run('{}:{}'.format(name,ver),name="preprocessRun1",remove=False,detach=True)
        except:
            container = dk.containers.get('preprocessRun1')
            container.remove(force=True)
            container = dk.containers.run('{}:{}'.format(name,ver),name="preprocessRun1",remove=False,detach=True)
            
        #
        # Extrair dado do Container
        #

        w = ''
        print(self.__class__,"Container {} Rodando ...".format(container.id))
        while w != 'exited':
            container.reload()
            w = container.status
        print(self.__class__,"Container {} Terminou".format(container.id))
        a,b = container.get_archive('src/data.pickle')

        try:
            os.mkdir('src/1-preprocess/{}/output/'.format(method))
        except:
            pass
        with open('src/1-preprocess/{}/output/data.tar'.format(method),'wb') as f:
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

        arquivo = tarfile.open('src/1-preprocess/{}/output/data.tar'.format(method))
        arquivo.extractall('src/1-preprocess/{}/output/'.format(method))
        arquivo.close()
        os.remove('src/1-preprocess/{}/output/data.tar'.format(method))

        #
        # Limpar a pasta
        #

        temp = os.listdir('src/1-preprocess/{}/{}'.format(method,'utils'))
        for x in temp:
            os.remove('src/1-preprocess/{}/{}/{}'.format(method,'utils',x))
        os.rmdir('src/1-preprocess/{}/{}'.format(method,'utils'))
        temp = os.listdir('src/1-preprocess/{}/{}'.format(method,'database'))
        for x in temp:
            os.remove('src/1-preprocess/{}/{}/{}'.format(method,'database',x))
        os.rmdir('src/1-preprocess/{}/{}'.format(method,'database'))

        return 0

    def processamento(self,method='method1'):
        name='process'
        
        #
        # Pegar arquivos do processo anterior
        #

        try:
            shutil.copy('src/1-preprocess/{}/output/data.pickle'.format(method),'src/2-process-intents/{}/'.format(method))
        except:
            print(self.__class__,"Arquivo de dados pre processados não encontrados")
            return 1
        
        #
        # Executar docker
        #
        
        dk = docker.from_env()
        dk.images.build(path ='src/2-process-intents/{}/'.format(method),tag="{}:{}".format(name,ver))

        try:
            container = dk.containers.run('{}:{}'.format(name,ver),name="processRun1",remove=False,detach=True)
        except:
            container = dk.containers.get('processRun1')
            container.remove(force=True)
            container = dk.containers.run('{}:{}'.format(name,ver),name="processRun1",remove=False,detach=True)
        
        print(self.__class__,"Container {} Rodando ...".format(container.id))
        w = ''
        while w != 'exited':
            container.reload()
            w = container.status
        print(self.__class__,"Container {} Terminou".format(container.id))
        a,b = container.get_archive('src/model/')

        try:
            os.mkdir('src/2-process-intents/{}/output/'.format(method))
        except:
            pass
        print(a)
        with open('src/2-process-intents/{}/output/data.tar'.format(method),'wb') as f:
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

        arquivo = tarfile.open('src/2-process-intents/{}/output/data.tar'.format(method))
        arquivo.extractall('src/2-process-intents/{}/output/'.format(method))
        arquivo.close()
        os.remove('src/2-process-intents/{}/output/data.tar'.format(method))

        #
        # Limpar pasta
        #

        os.remove('src/2-process-intents/{}/data.pickle'.format(method))

        return 0