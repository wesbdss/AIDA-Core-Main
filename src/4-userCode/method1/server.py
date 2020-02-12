import sys
import flask
from flask import request, jsonify
import numpy

"""
    Aqui deve conter a parte envolvida com o usuário de python, Provavelmente é bom criar um servidor de distribuição das falas (API)

"""

class Server():

    def bag_of_Words:
        pass


    def chat():
        print("Começe e falar com o bot")
        while True:
            inp = input("Você: ")
            if inp.lower() == quit:
                break 

            results = model.predict([arquivos.bag_of_words(s=inp,nome="lunaDefault")])[0] #words é do treinos
            results_index = numpy.argmax(results)
            tag = labels[results_index]

            if results[results_index]> 0.7:
                for tg in data["intents"]:
                    if tg['tag'] == tag:
                        responses = tg['responses']
            else: 
                print("Eu não entendi o que vc falou")

            print(random.choice(responses))
            print(results)

app = flask.Flask("Servidor API Bot")
app.config['DEBUG'] = True

@app.route('/',methods=['GET'])
def home():
    return "<h1>Pagina Inicial da Api</h1></br>Esta api tem propósito de hospedar um API de teste"
    
@app.route('/api/v1/intents/',methods=['GET'])
def index():
    parameters = request.args
    entrada = parameters.get('input')
    print(entrada)
    return entrada
app.run()