"""
    Creator : Wesley B. D. S. S.

    -- AVISOS:
    Todo método de IA, deve ter seu método run()
"""

import tensorflow
import tflearn
import sys
sys.path.insert(0, 'bib/adicionarIntents')
from preProcess import bagOfWords
import pickle

class process_tflearn():
     """
    Python 3.6.x
    Tensorflow == 1.14
    CUDA 10 
    Muito Antigo e não está em funcionamento
    
 """
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