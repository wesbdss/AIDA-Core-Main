import sys

"""
    Aqui deve conter a parte envolvida com o usuário de python, Provavelmente é bom criar um servidor de distribuição das falas (API)


    Flask - API rest
ou
    Servidor Websocket -- Vou implementar esse <-
"""



"""
    Funcionamento: 
    
    - O funcionamento vai ser dado de acordo com que os usuários vão se conectando, eles devem ter uma sessão.
    - Cada sessão nao deve ser influenciada por outra.
    - Sessões podem ser por conexao (Não guarda dados) ou por ID de conta (Guarda dados)

"""


import asyncio
import websockets
from libs.process import Process
from libs.preprocess import Preprocess
import json
import random

with open("arquivos/intents.json") as file:
    data = json.load(file)


class Server:
    def __init__(self):
        self.pcss = Process(load=True)
        self.ppcss = Preprocess()
    
    async def chat(self,sock,path):
        while True:
            words,labels,_,_ = self.pcss.carregarDado(dir='arquivos/data.pickle')

            #
            # Get dados do usuário
            #

            #
            # Importar processos
            #

            entrada =  await sock.recv()
            print(sock," > ",entrada)
            if entrada == 'quit': #fecha o servidor
                exit()

            #
            # Implementar requests Json
            #

            

            #
            # Carregar labels e tabela de palavras
            #

            results, results_index = self.pcss.predict(self.ppcss.preprocess(entrada,words))
            tag = labels[results_index]
            responses = []
            if results[results_index]> 0.6:
                for tg in data["intents"]:
                    if tg['tag'] == tag:
                        responses = tg['responses']
                await sock.send(random.choice(responses))
                print(random.choice(responses))
            else: 
                print("Eu não entendi o que vc falou")
                await sock.send("Não entendi o que vc falou!")
                #
                # Implementar o sistema de reaproveitamento de frases CSV
                #
            print(results)

    def main(self):
        print("Servidor rodando 0.0.0.0:10101")
        start_server = websockets.serve(self.chat,'0.0.0.0',10101)
        # server2 = websockets.serve(self.pass1,'localhost',10102)
        asyncio.get_event_loop().run_until_complete(start_server)
        # asyncio.get_event_loop().run_until_complete(server2)
        asyncio.get_event_loop().run_forever()
        
a = Server()
a.main()