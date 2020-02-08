
import tensorflow
import tflearn
import pickle

class process:
    def __init__(self):
        pass
    
    def main(self,training,output,epoch=1000,batch=8,):
        try:
            net = tflearn.input_data(shape=[None, len(training[0])])
            net = tflearn.fully_connected(net, 8)
            net = tflearn.fully_connected(net, 8)
            net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
            net = tflearn.regression(net)
            model = tflearn.DNN(net)
            with open('./model.tflearn','rb') as f:
                model = pickle.load(f)
            return 0
        except:
            model.fit(training, output, n_epoch=epoch, batch_size=batch, show_metric=True)
            with open('./model.tflearn','wb') as f:
                pickle.dump(model,f)
            return 0
        
            


