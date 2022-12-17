from structures.arvoreAVL import AVLTree
from modules.palavra import Palavra

class GamaException(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)

class Tema:
    def __init__(self, nome:str, teto:int, palavras:list[Palavra]):
        try:
            self.__nome = nome
            self.__avlPalavras = AVLTree()
            assert nome != '', teto <= len(palavras)-1
            self.__tetoSorteio = teto
            self.__preencherPalavras(palavras)
        except AssertionError:
            raise GamaException('Entradas (nome, teto e/ou palavras) inválidas!')


    def __str__(self):
        return f'{self.__nome} : {self.__strPalavras()}'

    @property
    def tetoSorteio(self) -> int:
        return self.__tetoSorteio

    @property
    def avlPalavras(self) -> int:
        return self.__avlPalavras.getNodes()

    @tetoSorteio.setter
    def tetoSorteio(self, teto:int) -> int:
        self.__tetoSorteio = teto
        return self.__tetoSorteio

    def __preencherPalavras(self, palavras:list[Palavra]):
        for palavra in palavras:
            self.__avlPalavras.insert(palavra)

    def __strPalavras(self):
        palavras = self.__avlPalavras.getNodes()
        temp = []
        for i in palavras:
            temp.append(str(i))
        return temp

    def __sortearPalavras(self) -> list:
        palavras = self.__avlPalavras.getNodes()
        palavras.shuffle()
        return palavras[:self.__tetoSorteio]
