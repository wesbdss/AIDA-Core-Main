import json
import os 
from unidecode import unidecode
import nltk
import pickle
import sys
nltk.download('punkt')
nltk.download('rslp')

identificador = '1'

from utils.findImports import FindImports

stemmer = nltk.stem.RSLPStemmer()
word_tokenize = nltk.tokenize.word_tokenize

class bagOfWords:
    def __init__(self):
        print("Modulo Iniciado: PreProcessando") ## mensagem importante
        path = os.getcwd()
        print ("O programa está sendo executado em -->  %s" % path)
        self.__fi = FindImports()
        self.main()
        print("Modulo Terminado: PreProcessando ")## mensagem importante

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
        with open("data.pickle","wb") as f:
            pickle.dump(dados,f)
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

if __name__ == "__main__":
    bagOfWords()