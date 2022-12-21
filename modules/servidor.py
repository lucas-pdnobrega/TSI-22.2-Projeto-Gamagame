from modules.tema import Tema
import random

class GamaException(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)

class Server():
    def __init__(self, temas:list[Tema]):
        self.__temas = temas
        self.__escolhido = None
        self.__nomeatual = ''
        self.__atual = []
    
    def __str__(self):
        temas = []
        for i in self.__temas:
            temas.append(str(i))
        return str(temas)
        
    @property
    def temas(self) -> list:
        return self.__temas

    @property
    def escolhido(self) -> int:
        return self.__escolhido

    @property
    def nomeatual(self) -> str:
        return self.__nomeatual

    @property
    def atual(self) -> list:
        return self.__atual

    @escolhido.setter
    def escolhido(self, index:int):
        try:
            assert index >= 0 and index <= len(self.__temas)
            self.__escolhido = index
        except:
            raise GamaException('Índice inválido!')

    def sortearTema(self):
        '''Método que sorteia o tema da partida.'''
        self.__escolhido = random.randint(0, len(self.__temas)-1)
        self.__nomeatual = self.__temas[self.__escolhido].nome
        self.__atual = self.__temas[self.__escolhido].sortearPalavras(3)
        # [Palavra#1, Palavra#2, ...]

    def verifyPalpite(self, palpite:str)-> bool:
        '''Método utilizado para verificar se o palpite enviado está correto ou não.'''
        try:
            assert palpite != ''
            palavras = self.__atual
            for i in range(len(palavras)):
                if palpite.lower() == palavras[i].termo.lower():
                    self.__atual.pop(i)
                    return True
            return False
        except AssertionError:
            raise GamaException('Palpite inválido!')

    