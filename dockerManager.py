import docker

class managerDocker:
    client = None
    def __init__(self):
        self.client = docker.from_env()
        print("Entrou")
    
    def list_containers(self):
        container = self.client.containers.list()
        return container
    
    def get_Container(self,id='',logs=False):
        if len(id)<=1:
            print("Nome do container vazio")
            return
        if id in self.list_containers():
            container = self.client.containers.get(id)
            if logs:
                for line in container.logs(stream=True):
                    print (line.strip())


t = managerDocker()
print(t.list_containers())
t.get_Container(id='c8dc8984a7',logs=True)



        