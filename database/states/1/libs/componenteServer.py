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
import json
import random
from libs.preprocess import Preprocess
from libs.process import Process 
# from libs.AIDA-fluxo.fluxo import Fluxo
class ComponenteServer:
    def __init__(self,fluxo=False):
        self.fluxoInd = fluxo
        # self.fluxo = Fluxo('arquivos/fluxo.yaml')
        self.pcss = Process(load=True)
        self.ppcss = Preprocess()
        self.words,self.labels,_,_ = self.pcss.carregarDado(dir='arquivos/data.pickle')
        with open("arquivos/intents.json") as file:
            self.data = json.load(file)
            file.close()
    
    def response(self, entrada = ''):
        if self.fluxoInd:
            pass
            #
            # Implementar com fluxo de dados
            #

        else:
            preprocesso = self.ppcss.preprocess(entrada,self.words)
            results, results_index = self.pcss.predict(preprocesso)
            tag = self.labels[results_index]
            if results[results_index] > 0.6:
                for tg in self.data["intents"]:
                    if tg['tag'] == tag:
                        responses = tg['responses']
                return random.choice(responses)+" --> {} - {}".format(self.labels[results_index],results[results_index])
            else:
                #
                # Salvar Entradas Não Aceitas (Reaproveitamento CSV)
                #
                return "Não entendi o que vc falou --> {} - {}".format(self.labels[results_index],results[results_index])
