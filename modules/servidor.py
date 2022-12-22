from modules.tema import Tema
from typing import List
import random

class GamaException(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)

class Server():
    '''
    Classe que gerencia os dados do servidor.
    '''
    #temas forma uma lista 
    def __init__(self, temas:List[Tema]):
        self.__temas = temas
        self.__escolhido = None
        self.__temaAtual = ''
        self.__respostas = []
    
    def __str__(self):
        temas = []
        for i in self.__temas:
            temas.append(str(i))
        return str(temas)
        
    @property
    def temas(self) -> List:
        return self.__temas

    @property
    def escolhido(self) -> int:
        return self.__escolhido

    @property
    def temaAtual(self) -> str:
        return self.__temaAtual

    @property
    def respostas(self) -> List:
        return self.__respostas

    @escolhido.setter
    def escolhido(self, index:int):
        '''Método para substituir o valor do índice do tema escolhido.'''
        try:
            assert index >= 0 and index <= len(self.__temas)
            self.__escolhido = index
        except:
            raise GamaException('Índice inválido!')

    def sortearTema(self):
        '''Método que sorteia o tema da partida.'''
        self.__escolhido = random.randint(0, len(self.__temas)-1)
        self.__temaAtual = self.__temas[self.__escolhido].nome
        self.__respostas = self.__temas[self.__escolhido].sortearPalavras(5)

    def verifyPalpite(self, palpite:str) -> bool:
        '''Método utilizado para verificar se o palpite enviado está correto ou não.'''
        try:
            assert palpite != ''
            palavras = self.__respostas
            for i in range(len(palavras)):
                if palpite.lower() == palavras[i].termo.lower():
                    print(palavras[i].termo.lower())
                    self.__respostas.pop(i)
                    return True
            return False
        except AssertionError:
            raise GamaException('Palpite inválido!')