"""
    Modulo para rodar no docker -- sujeito a alterações
"""
import tensorflow
import tflearn
import numpy
import pickle
import os

class Process:
    def __init__(self,modeldir='arquivos/model.tflearn'):
        if os.path.exists('arquivos'):
            self.model = self.modelo(dir='arquivos/data.pickle')
            self.model.load(modeldir)
        else:
            self.main()

    def carregarDado(self,dir='data.pickle'):
        try:
            with open(dir,'rb') as f:
                words,labels,training,output = pickle.load(f)
                f.close()
            return words,labels,training,output
        except Exception:
            print(self.__class__,"Arquivo data não encontrado")
            return 1
    
    #
    # Método obrigatório!
    #
    def predict(self,entrada):
        #entrada tem que estar modelada e preprocessad
        results = self.model.predict([entrada])[0]
        results_index = numpy.argmax(results)
        return results, results_index
    #
    # -- 
    #


    def modelo(self,dir='data.pickle'):
        _,_,training,output = self.carregarDado(dir)
        tensorflow.reset_default_graph()
        net = tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
        net = tflearn.regression(net)
        model = tflearn.DNN(net)
        return model

    def main(self,epoch=1000,batch=8):
        self.model = self.modelo()
        _,_,training,output = self.carregarDado()
        self.model.fit(training, output, n_epoch=epoch, batch_size=batch, show_metric=True)
        try:
            os.mkdir('../output')
        except Exception:
            pass
        self.model.save('../output/model.tflearn') #model.load() nao esta funcionando


if __name__ == "__main__":
    a = Process()
    a.main()
