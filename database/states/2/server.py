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
import json
from libs.componenteServer import ComponenteServer

class Server:
    
    def jsonEncode(self,res,label,acc,data):
        response =  {
                "response": str(res),
                "label" :str(label),
                "accuracy": str(acc),
                "bot": data
            }
        response = json.dumps(response,ensure_ascii=False)
        return response

    async def chat(self,sock,path):
        component = ComponenteServer(fluxo=False)
        a,b,c,d = component.init()
        await sock.send(self.jsonEncode(a,b,c,d))
        while True:
            entrada = await sock.recv()
            print(sock," > ",entrada)
            if entrada == 'quit': #fecha o servidor
                exit()
            a,b,c,d = component.response(entrada)
            await sock.send(self.jsonEncode(a,b,c,d))

    def main(self):
        print("Servidor rodando 0.0.0.0:10101")
        start_server = websockets.serve(self.chat,'0.0.0.0',10101)
        # server2 = websockets.serve(self.pass1,'localhost',10102)
        asyncio.get_event_loop().run_until_complete(start_server)
        # asyncio.get_event_loop().run_until_complete(server2)
        asyncio.get_event_loop().run_forever()
        
a = Server()
a.main()