import sys
sys.path.insert(0, 'lib/adicionarIntents')
from adicionarIntents import arquivos

"""
    Aqui deve conter a parte envolvida com o usuário de python, Provavelmente é bom criar um servidor de distribuição das falas (API)

"""


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