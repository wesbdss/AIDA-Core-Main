"""
    Creator : Wesley B. D. S. S.
"""
import json
import sys
sys.path.insert(0, 'bib/adicionarIntents') #arrumar
from adicionarIntents import arquivos
import numpy
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import pickle


"""
            ----- Descrição -----

    - Cada classe criada é um tipo de preprocessamento;
    - O preprocessamento deve criar um arquivo com o nome desejado, que será identificado durante todo o processo
    - Os dados devem ser salvo com pickle para leitura posterio;
    - Cada etapa é independente
    - Pasta de correspondencia é 'data'
    - Deve haver no mínimo um intents.json na pasta


"""


class bagOfWords(): 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self = '',nome ='lunaDefault',intentArq = 'intents'):
        dir = "./data/"+intentArq+".json"

        with open(dir,encoding='utf-8') as file:
            dados = json.load(file)

        try:
            with open("data/"+nome+".pickle") as f:
                words,labels,training,output = pickle.load(f)

        except Exception:
            words = []
            labels = []
            docs_x = []
            docs_y = []

            for intent in dados['intents']:
                for pattern in intent['patterns']:
                    wrds = nltk.word_tokenize(pattern)
                    words.extend(wrds)
                    docs_x.append(pattern)
                    docs_y.append(intent['tag'])
                if intent['tag'] not in labels:
                    labels.append(intent['tag'])
                
            words = [stemmer.stem(w.lower()) for w in words if w != '?']
            words = sorted(list(set(words)))

            labels = sorted(labels)
            print(words)
            training = []
            output = []

            out_empty = [0 for _ in range(len(labels))]

            for x, doc in enumerate(docs_x):
                bag = []
                wrds = [stemmer.stem(w) for w in doc]
                for w in words:
                    if w in wrds:
                        bag.append(1)
                    else:
                        bag.append(0)

                output_row = out_empty[:]
                output_row[labels.index(docs_y[x])] = 1

                training.append(bag)
                output.append(output_row)

            training = numpy.array(training)
            output = numpy.array(output)
           
            with open("data/"+nome+".pickle","wb") as f:
                pickle.dump((words,labels,training,output),f)


    def bag_of_words(self = '',s = '',nome = 'lunaDefault'):
        try:
            with open("data/"+nome+".pickle") as f:
                words,labels,training,output = pickle.load(f)
        except:
            self.run(nome=nome)
            with open("data/"+nome+".pickle") as f:
                words,labels,training,output = pickle.load(f)

        if s == '':
            print("Sentença fazia")
            return 0
        bag=[0 for _ in range(len(words))]
        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(words.lower()) for word in s_words]

        for se in s_words:
            for i,w in enumerate(words):
                if w == se:
                    bag[i] = 1
        
        return numpy.array(bag)


bagOfWords.run()
