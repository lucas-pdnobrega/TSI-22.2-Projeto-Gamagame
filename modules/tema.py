from structures.arvoreAVL import AVLTree
from modules.palavra import Palavra
import random

class GamaException(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)


class Tema:
    ''' 
    Classe que armazena várias palavras organizadas nível de dificuldade.
    '''
    def __init__(self, nome:str, palavras:list[Palavra]):
        try:
            assert nome != '' and len(palavras) > 0
            self.__nome = nome
            self.__avlPalavras = AVLTree()
            self.__preencherPalavras(palavras)
        except AssertionError:
            raise GamaException('Entradas (nome, e/ou palavras) inválidas!')

    def __str__(self):
        return f'{self.__nome} : {self.__strPalavras()}'

    @property
    def nome(self) -> str:
        '''Retorna o nome da árvore de temas'''
        return self.__nome

    @property
    def avlPalavras(self) -> list[Palavra]:
        '''Retorna a lista de palavras que está na árvore'''
        return self.__avlPalavras.getNodes()

    def __preencherPalavras(self, palavras:list[Palavra]):
        '''Insere novas palavras na árvore de palavras'''
        for palavra in palavras:
            self.__avlPalavras.insert(palavra)

    def __strPalavras(self):
        '''Método auxiliar utilizado no método especial __str__'''
        palavras = self.__avlPalavras.getNodes()
        temp = []
        for i in palavras:
            temp.append(str(i))
        return temp

    def addPalavra(self, peso:int, termo:str):
        '''
        Adiciona uma nova palavra àquele tema. São passados como argumentos
        o peso dessa palavra e o seu termo (a string palavra em si).
        '''
        try:
            assert peso > 0 and termo != '' and str(Palavra(peso, termo)) not in (self.__strPalavras())
            self.__avlPalavras.insert(Palavra(peso, termo))
        except AssertionError:
            raise GamaException('Entradas (peso e/ou termo) inválidas!')

    def delPalavra(self, peso:int, termo:str):
        '''
        Deleta uma palavra que está contida em um tema. São passados como
        argumentos o peso dessa palavra e o seu termo(a string palavra em si).
        '''
        try:
            assert peso > 0 and termo != '' and str(Palavra(peso, termo)) in (self.__strPalavras())
            self.__avlPalavras.delete(Palavra(peso, termo))
        except AssertionError:
            raise GamaException('Palavra inválida! Não está contida no tema!')

    def sortearPalavras(self, teto:int) -> list:
        '''Sorteia as palavras de um tema. A quantidade de palavras é limitada pelo parâmetro inteiro "teto".'''
        try:
            assert teto > 0 and teto <= len(self.__strPalavras())
            palavras = self.__avlPalavras.getNodes()
            random.shuffle(palavras)
            return palavras[:teto]
        except:
            raise GamaException('Entradas (teto) inválidas!')