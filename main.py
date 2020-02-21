"""
    Creator : Wesley B. D. S. S.
"""

"""
    Etapas Treinamento ::
    1 - Adicionar a base
    2 - Pre processamento (Pode personalizar)
    3 - Treinamento (Pode Personalizar)
    4 - Uso dados processados por IA


    funciona com a seguinte estrutura: 

        lunaChatbot:
            - data (Onde fica os dados necessários para treinamento)
            - lib (Onde fica os métodos)
        main
"""


"""
 -> aqui deve ter as criações das pastas importantes :
  - data
  - model
  - lib
  - userCode
 -> Aqui deve ser gerado todo os códigos utilizado pelo usuário
"""

from src.orquestrador import Orquestrador
from utils import findImports


class Main:
    def __init__(self):
        pass
    
    def main(self):
        orq = Orquestrador()
        # orq.preprocessamento()
        # orq.processamento()
        orq.userCode()
        print("sucesso")


if __name__ == "__main__":
    m = Main()
    m.main()