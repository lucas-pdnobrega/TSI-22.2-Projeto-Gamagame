# para cada thread, criar um objeto jogador
from structures.pilhaEncadeada import Pilha

class GamaException(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)

class Jogador():
    def __init__(self, nome: str) -> None:
        self.__nome = nome
        self.__pontuacao = 0
        # número de acertos por usuário
        self.__tentativas = Pilha()

    def __str__(self):
        return f"Nome: {self.__nome}\nPontuação: {self.__pontuacao}\nTentativas: {self.__tentativas}"

    def pontuar(self) -> None:
        self.__pontuacao += 10
    
    def addTentativa(self, tentativa:str) -> bool:
            if not self.__tentativas.existe(tentativa):
                self.__tentativas.empilha(tentativa)
                return True
            return False
            

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def pontuacao(self) -> int:
        return self.__pontuacao

    @property
    def tentativas(self) -> 'Pilha':
        return self.__tentativas