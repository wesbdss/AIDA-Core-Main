import sys

"""
    Aqui deve conter a parte envolvida com o usuário de python, Provavelmente é bom criar um servidor de distribuição das falas (API)


    Flask - API rest
ou
    Servidor Websocket -- Vou implementar esse <-
"""

class Server1():



    def chat():
        print("Começe e falar com o bot")
        while True:
            inp = input("Você: ")
            if inp.lower() == quit:
                break 

            results = model.predict([arquivos.bag_of_words(s=inp,nome="lunaDefault")])[0] #words é do treinos
            results_index = numpy.argmax(results)
            tag = labels[results_index]

            if results[results_index]> 0.7:
                for tg in data["intents"]:
                    if tg['tag'] == tag:
                        responses = tg['responses']
            else: 
                print("Eu não entendi o que vc falou")

            print(random.choice(responses))
            print(results)


"""
    Funcionamento: 
    
    - O funcionamento vai ser dado de acordo com que os usuários vão se conectando, eles devem ter uma sessão.
    - Cada sessão nao deve ser influenciada por outra.
    - Sessões podem ser por conexao (Não guarda dados) ou por ID de conta (Guarda dados)

"""


import asyncio
import websockets


"""
CLIENTE EXEMPLO

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
class Server:
    async def pass1(self,websocket,path):
        print(path)
        print(websocket)
        tes = await websocket.recv()
        print(tes)
        await websocket.send('Blz mlk')

    def main(self):
        start_server = websockets.serve(self.pass1,'localhost',10101)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    
a = Server()
a.main()       