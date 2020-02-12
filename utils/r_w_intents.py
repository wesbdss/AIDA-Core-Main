"""
    Creator : Wesley B. D. S. S.
"""

import json
import os


class R_w_intents():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def readJson(self='',dir=''): # lê o arquivo json inteiro

        if dir == '':
            dir = "./data/intents.json"

        if not os.path.exists(dir): 
            print("O diretório "+dir+ " não existe ")
            print(os.listdir())
        else:
            with open(dir) as data:
                dados = json.load(data)
            return dados
        
    def writeIntent (self ='', tag ='', value = '',dir= ''): #escreve uma tag e um valor no arquivo
        if dir == '':
            dir = "./data/intents.json"
        if tag == '' or value == '':
            print("Um dos valores estão em Branco")
            return ''

        else: 
            with open(dir,encoding='utf-8') as data:
                dados = json.load(data)
            find = False
            for x in range(0,len(dados['intents'])):
                if tag in dados['intents'][x]['tag']:
                    if not value in dados['intents'][x]['patterns']:
                        dados['intents'][x]['patterns'].append(value)
                    find = True
                    break
            if not find:
                dados['intents'].append({'tag': tag,'patterns': [value],'responses':['']})
            with open(dir,'w',encoding='utf-8') as data:
                json.dump(dados,data,indent= 3,ensure_ascii=False)
            return 'OK'
        
    def readIntent (self = '',tag ='',dir=''): #encontra a tag em um arquivo json
        if dir == '':
            dir = "./data/intents.json"
        if tag == '':
            print("Tag vazia")
            return ''
        dados = ''
        with open(dir,encoding='utf-8') as data:
            dados = json.load(data)
        
        for x in range(0,len(dados['intents'])):
            if dados['intents'][x]['tag'] == tag:
                return dados['intents'][x]
        return ''