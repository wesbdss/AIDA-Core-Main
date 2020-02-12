"""
    Modulo para rodar no docker -- sujeito a alterações
"""
import tensorflow
import tflearn
import pickle

class Process:
    def __init__(self):
        pass

    def carregarDado(self,dir='data.pickle'):
        try:
            with open(dir,'rb') as f:
                words,labels,training,output = pickle.load(f)
                f.close()
            return training,output
        except Exception:
            print(self.__class__,"Arquivo data não encontrado")
            return 1

    def modelo(self,epoch=1000,batch=8):

        training,output = self.carregarDado()
        tensorflow.reset_default_graph()
        net = tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
        net = tflearn.regression(net)
        model = tflearn.DNN(net)
        return model

    def main(self,epoch=1000,batch=8):
        model = self.modelo(epoch=epoch,batch=batch)
        training,output = self.carregarDado()
        model.fit(training, output, n_epoch=epoch, batch_size=batch, show_metric=True)
        model.save('./model/model.tflearn') #model.load() nao esta funcionando


if __name__ == "__main__":
    a = Process()
    a.main()


