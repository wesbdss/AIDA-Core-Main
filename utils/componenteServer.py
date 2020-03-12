"""
    ------ Lib de métodos padrões para servidores ------

    Objetivo desse arquivo é juntar todos os acessos necessários aos métodos de preprocessamento e processamento, alem do fluxo de dados e etcs
    tudo em apenas uma classe ou conjunto de classes


"""


"""
    Procedimentos:
        leitura dos dados enviados
        limpeza dos dados
        entrada no processamento dos dados
        entrada no fluxo de dados
        entrega da resposta
"""

"""
    Estrutura temporária:
    lib.py
    utils/
    libs/
        preprocess
        process
        fluxo
    arquivos/
        data
"""

from libs.preprocess import Preprocess
from libs.process import Process 

class ComponenteServer:
    def __init__(self,fluxo=False):
        self.fluxo = fluxo
        self.pcss = Process(load=True)
        self.ppcss = Preprocess()
        with open("arquivos/intents.json") as file:
            self.data = json.load(file)
            file.close()
    
    def load(self):
        self.words,self.labels,_,_ = self.pcss.carregarDado(dir='arquivos/data.pickle')

    def response(self):
        if fluxo:

        else:
            preprocesso = self.ppcss.preprocess(entrada,self.words)
            results, results_index = self.pcss.predict(preprocesso)
            tag = labels[results_index]
            if results[results_index] > 0.6:
                for tg in self.data['intents']
                    if tg['tag'] == tg['responses']
                return random.choice(responses)
            else:
                #
                # Salvar Entradas Não Aceitas
                #
                return "Não entendi o que vc falou"

    

    
