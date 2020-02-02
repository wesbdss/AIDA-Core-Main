import tensorflow
import tflearn
import sys
sys.path.insert(0, 'bib/adicionarIntents')
from preProcess import bagOfWords



"""
            ----- Descrição -----

    - Cada classe criada é um tipo de processamento dos dados;
    - O processamento deve usar o nome do arquivo criado anteriormente para modularizar os arquivos
    - Os dados devem ser salvo com pickle para leitura posterior;
    - Cada etapa é independente


"""


class process_tflearn():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self='',epoch= 1000, nome="lunaDefault"):
        try:
            with open("data/"+nome+".pickle","rb") as f:
                words,labels,training,output = pickle.load(f)
        except Exception:
            bagOfWords.run(nome=nome)
            with open("data/"+nome+".pickle","rb") as f:
                words,labels,training,output = pickle.load(f)
        
        tensorflow.reset_default_graph()
        net= tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net,8)
        net = tflearn.fully_connected(net,8)
        net = tflearn.fully_connected(net,len(output[0]),activation="softmax")
        ner = tflearn.regression(net)

        model = tflearn.DNN(net)
        try:
            model.load("model/"+nome+"model.tflearn")
        except:
            model.fit(training, output, n_epoch=epoch, batch_size=8,show_metric=True)
            model.save("model/"+nome+".model.tflearn")

    


process_tflearn.run()
