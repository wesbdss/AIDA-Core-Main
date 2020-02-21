import sys

"""
    Aqui deve conter a parte envolvida com o usuário de python, Provavelmente é bom criar um servidor de distribuição das falas (API)


    Flask - API rest
ou
    Servidor Websocket -- Vou implementar esse <-
"""
"""
CLIENTE EXEMPLO PYTHON

import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
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
        self.pcss = Process()
        self.ppcss = Preprocess()
        self.words,self.labels,_,_ = self.pcss.carregarDado(dir='arquivos/data.pickle')
    async def pass1(self,websocket,path):
        print(path)
        print(websocket)
        while 1:
            tes = await websocket.recv()
            print(tes)
            await websocket.send('Blz mlk')
    
    async def chat(self,sock,path):

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

        results, results_index = self.pcss.predict(self.ppcss.preprocess(entrada,self.words))
        tag = self.labels[results_index]

        if results[results_index]> 0.6:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
            await sock.send(random.choice(responses))
        else: 
            print("Eu não entendi o que vc falou")
            #
            # Implementar o sistema de reaproveitamento de frases CSV
            #
        print(random.choice(responses))
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