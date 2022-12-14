# para cada thread, criar um objeto jogador
from pilhaEncadeada import Pilha

class Jogador():

    def __init__(self, nome: str, pontuacao: int) -> None:
        self.__nome = nome
        self.__pontuacao = pontuacao
        # número de acertos por usuário
        self.__tentativas = Pilha()
    
    def pontuar(self) -> None:
        self.__pontuacao += 10

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def pontuacao(self) -> int:
        return self.__pontuacao

    @property
    def tentativas(self) -> 'Pilha':
        return self.__tentativas
        