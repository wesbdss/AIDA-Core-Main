import socket
import threading
import json

"""
Esse programa ´foi construido para fazer a comunicação e passagem de dados atraves de um canal. 

So é válido para 2 clientes
"""
class ThreadCon(threading.Thread):
    def __init__(self, group=None, name=None,args=(),):
        threading.Thread.__init__(self, group=group, name=name)
        self.args = args

    def run(self):
        print(self.getName()," -- Iniciado")
        while True:
            print("Servidor >> Esperando quem vai enviar ")
            conn,addr = self.args[0].accept()
            data = conn.recv(1024)
            print("Servidor >>",data.decode('utf-8'))
            f = conn.recv(1024)
            conn.send(b'Ok')
            # Parte do Receptor
            print("Servidor >> Esperando quem vai receber ")
            conn2,addr2 = self.args[0].accept()
            data2 = conn.recv(1024)
            print("Servidor >>",data2.decode('utf-8'))
            conn2.send(f)

            # Fecha as duas conexões
            conn2.close()
            conn.close()
            break
        print(self.getName()," -- Terminado")


class Conexao():
    def __init__(self):
        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ender1 = ('localhost',7887)
        
    def servidor(self):
        self.sock1.bind(self.ender1)
        self.sock1.listen(2)
        server = ThreadCon(name = "Servidor Thread",args=(self.sock1,))
        server.start() 
        

    def send(self,type=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        """
        Types -> São identificações dos processos conectados, serve apra definir para quem cada dado deve ser enviado.

        Types:
            preprocess - 1
            process - 2
        """

        try:
            sock.connect(self.ender1)
            print("SENDER >> Conectando a ", self.ender1)
            sock.send(type.encode('utf-8'))
            with open("intents.json","r",encoding='utf-8') as f:
                sock.send(f.read().encode('utf-8'))
            response = sock.recv(1024)
            sock.close()
            print("SENDER >> Arquivo Enviado")
            return 'OK'
        except:
            print("Nenhum Servidor Aberto -- Send")

        

    def receive(self,type=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(self.ender1)
            print("RECEIVER >> Conectando a ", self.ender1)
            sock.send(type.encode('utf-8'))
            response = sock.recv(1024)
            print(response.decode('utf-8'))
            print("SENDER >> Arquivo Recebido")
            return response.decode('utf-8')
        except:
            print("Nenhum Servidor Aberto -- Receive")

a = Conexao()
a.servidor()
a.send(type="preprocess")
a.receive(type="process")


    