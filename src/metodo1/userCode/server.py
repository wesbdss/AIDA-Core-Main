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
import process
import nltk
import json
import random
import numpy
nltk.download('punkt')
nltk.download('rslp')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

with open("./intents.json") as file:
    data = json.load(file)


class Server:
    async def pass1(self,websocket,path):
        print(path)
        print(websocket)
        while 1:
            tes = await websocket.recv()
            print(tes)
            await websocket.send('Blz mlk')
    
    async def chat(self,sock,path):
        entrada =  await sock.recv()
        print(sock," > ",entrada)
        if entrada == 'quit': #fecha o servidor
            exit()
        pcss = process.Process()
        model = pcss.modelo()
        words,labels,_,_ = pcss.carregarDado()
        model.load('./model/model.tflearn')
        results = model.predict([self.bag_of_words(entrada,words)])[0] #words é do treinos
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        if results[results_index]> 0.7:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
            await sock.send(random.choice(responses))
        else: 
            print("Eu não entendi o que vc falou")

        print(random.choice(responses))
        print(results)

    def bag_of_words(self,s, words):
        bag = [0 for _ in range(len(words))]

        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1
        return numpy.array(bag)

    def main(self):
        start_server = websockets.serve(self.chat,'localhost',10101)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
        

a = Server()
a.main()