import os
import sys
import platform

class FindImports:
    def __init__(self):
        self.local()
        self.__found = []
        pass
    
    def imports(self,module=''): #importa o modulo específico no path adicionado em tempo de execução
        if module:
            self.pathImport('.')
            lists=self.pathList()
            for x in lists:
               if module == x[:-3]:
                    module = module[:1].upper()+module[1:]
                    try:
                        print("Modulo solicitado: ",module,' __import__("{}").{}'.format(x[:-3],module+'()'))
                        return eval('__import__("{}").{}'.format(x[:-3],module+'()'))
                    except Exception as ex:
                        print(ex)
                        print("O módulo solicitado não possui o mesmo nome da Classe, alem de possuir primeira letra maiuscula")
                        return -1
                    
        print("ERR >> modulo não existe",self.pathList())
        return -1
            

    def pathImport(self,dir=''): # importa um path para ser acessível
        (dirname,_) = self.local()
        try:
            if platform.system == 'Windows':
                dir = dir.replace('/','\\')
            sys.path.insert(0,dirname+dir)
            return dirname+dir
        except:
            print("Não foi possível inserir o path")

    def local(self): # retorna o local e atualiza os paths
        dirname, self.basename = os.path.split(os.path.abspath(__file__))
        self.__paths = sys.path[:]
        try:
            self.__paths.remove(dirname)
        except:
            pass
        return (dirname,self.basename)

    def getDirname(self,name=''): # pega o diretorio completo do arquivo solicitado
        r,d = self.pathList(dir=True)
        for i,data in enumerate(r):
            if name in data:
                if platform.system == 'Windows':
                    return d[i]+"\\"+name
                return d[i]+"/"+name
        print("ERR >> Arquivo não existente, tente adicionar no path (pathImport)")

    def pathList(self,dir=False): # lista os paths adicionados
        self.pathImport('.')
        lista = [y for y in sys.path if y not in self.__paths]
        r = []
        d = []
        for i,x in enumerate(lista):
            z = [y for y in os.listdir(x) if y not in  ['__pycache__', self.basename]]
            r.append(z)
            d.append(x)
        if dir:
            return r,d
        y = [x for x in r if type(x)==list]
        y = [z for x in y for z in x]
        return y
    
    def findDiretory(self,arq=[],local='.'):
        if arq == []:
            return self.__found
        else:
            path = os.getcwd()
            ignore = ['.git','.gitignore','.vs','.vscode','README.md','LICENSE','Dockerfile']
            arquivos = []
            pastas = []
            lista = os.listdir(local)
            lista= [x for x in lista if x not in ignore]
            for x in lista:
                if x.count('.') > 0:
                    arquivos.append(x)
                else:
                    pastas.append(x)
            for x in arq:
                if x in arquivos:
                    self.__found.append({"name": x,'dir':path+'\\'+local+"\\"+ x})
                    arq.remove(x)
            for x in pastas:
                self.findDiretory(arq = arq,local= local+'\\'+x)
        return self.__found
            


