"""

    Código feito para rodar dentro do Docker

"""

import json
import os 
from unidecode import unidecode
import nltk
import pickle
import sys
import numpy

nltk.download('punkt')
nltk.download('rslp')
stemmer = nltk.stem.RSLPStemmer()
word_tokenize = nltk.tokenize.word_tokenize

class Preprocess:
    def __init__(self):
        print("Modulo Iniciado: PreProcessando") ## mensagem importante
        path = os.getcwd()
        print ("O programa está sendo executado em -->  %s" % path)

    def main(self):
        # Pegar dados
        with open('database/intents.json',"r",encoding="UTF-8") as f:
            intents = json.load(f)
        
        words = []
        labels = []
        docs_x = []
        docs_y = []
        stopwords = ['!','?']

        for intent in intents['intents']:
            for pattern in intent['patterns']:
                plv = word_tokenize(pattern)
                plv = [unidecode(w.lower()) for w in plv]
                words.extend(plv)
                docs_x.append(plv)
                docs_y.append(intent['tag'])
            
            if intent['tag'] not in labels:
                labels.append(intent['tag'])
        # words = [stemmer.stem(w) for w in words if w not in stopwords]
        words = [w for w in words if w not in stopwords]
        words = sorted(list(set(words)))
        labels = sorted(labels)
        (training, output) = self.bagwords(labels,docs_x,docs_y,words)
        dados = (words,labels,training,output)
        print("Salvo em ",os.getcwd())
        try:
            os.mkdir('../output')
        except:
            pass
        with open("../output/data.pickle","wb") as f:
            pickle.dump(dados,f)
        print(self.__class__,"Módulo de preprocessamento terminado")
        return (training,output)

    def bagwords(self,labels,docs_x,docs_y,words):
        training = []
        output = []

        out_vazio = [0 for _ in range(len(labels))]

        for x, doc in enumerate(docs_x):
            bag= []
            plv = [w.lower() for w in doc]
            for w in words:
                if w in plv:
                    bag.append(1)
                else:
                    bag.append(0)
            
            output_row = out_vazio[:]
            output_row[labels.index(docs_y[x])] =1

            training.append(bag)
            output.append(output_row)

        return training, output

    #
    # Método Obrigatório em preprocessamento
    #
    def preprocess(self,s, words): # Bag of word individual
        bag = [0 for _ in range(len(words))]

        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1
        return numpy.array(bag)

if __name__ == "__main__":
    a = Preprocess()
    a.main()