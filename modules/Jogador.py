# para cada thread, criar um objeto jogador
from structures.pilhaEncadeada import Pilha

class GamaException(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)

class Jogador():
    '''
    Classe jogador para guardar as informações sobre um jogador de uma partida do Gamagame.
    '''
    def __init__(self, nome: str) -> None:
        self.__nome = nome
        self.__pontuacao = 0
        # número de acertos por usuário
        self.__tentativas = Pilha()

    def __str__(self):
        return f'{self.__nome}[{self.__pontuacao}] ({self.__tentativas})'

    @property
    def nome(self) -> str:
        '''Retorna o nome de um jogador.'''
        return self.__nome

    @property
    def pontuacao(self) -> int:
        '''Retorna a pontuação de um jogador.'''
        return self.__pontuacao

    @property
    def tentativas(self) -> Pilha:
        '''Retorna a pilha de tentativas de um jogador.'''
        return self.__tentativas

    def pontuar(self) -> None:
        '''
        Incrementa a pontuação do jogador.
        '''
        self.__pontuacao += 10
    
    def addTentativa(self, tentativa:str) -> bool:
        '''Adiciona as tentativas do jogador em sua pilha de tentativas.'''
        if not self.__tentativas.existe(tentativa):
            self.__tentativas.empilha(tentativa)
            return True
        return False