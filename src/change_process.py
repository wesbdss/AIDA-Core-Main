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


"""
import sys
sys.path.insert(0, 'bib/AI_Class')
import os
import platform


class selectIA():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def main(self,method= 'basic'):
        try: 
            _locales = [w[:-3] for w in os.listdir("bib/AI_Class/") if (w[-3:] == '.py')]
        except:
            print("Não existe a pasta 'bib/AI_Class/'")
        
        if len(_locales) == 0: 
            print("Não há metodos na pasta 'bib/AI_Class/'")

        if method in _locales:
            _ia = __import__(method)
            _ia.process_keras.run()

    def list(self):
        print(platform.system())
        arquivos = os.listdir('./process/')
        print(arquivos)
        return arquivos


            

selectIA.list(None)
