import socket
import sys

class Cliente():

    def __init__(self, host: str, port: int) -> None:
        self.__host = host
        self.__port = port

    def getHost(self):
        '''Get'''
        return self.__host
    
    def pontuacao(self, pontos: int) -> None:
        self.pontos = pontos
        