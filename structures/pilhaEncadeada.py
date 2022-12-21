from typing import Any

class PilhaException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class No:
    def __init__(self, conteudo: Any):
        self.conteudo = conteudo
        self.prox = None

    def __str__(self):
        return str(self.conteudo)


class Pilha:

    '''
            ~ RECEITA DE BOLO PARA PERCORRER UMA PILHA/LISTA ENCADEADA ~
    
        cursor = self.__head #Armazene o nó atual numa variável qualquer
        while (CONDIÇÃO): #EX : cursor.prox != None 
            cursor = cursor.prox #Atualize o valor da variável para ser o próximo nó encadeado


        ======================================================================================

        deve ter mais formas de mexer com encadeamento ...
        fazer a head apontar pro tail e o tail apontar pro head faz uma estrutura circular
        cabecinha com bundinha & bundinha com cabecinha  :)

    '''

    def __init__(self):
        self.__head = None
        self.__tamanho = 0

    def estaVazia(self)->bool:
        return self.__head == None

    def tamanho(self)->int:
        return self.__tamanho
    
    def topo(self) -> Any:
        return self.__head.conteudo

    def __len__(self)->int:
        return self.__tamanho

    def elemento(self, conteudo:int)->Any:
        #Retorna a carga armazenada no nó na posição N
        atual = self.__head
        while (atual):
            if atual.conteudo == conteudo:
                return True
            atual = atual.prox
        return False
    
    def busca(self, conteudo:Any)->int:
        #Retorna a posição do nó cuja conteúdo corresponde à consulta
        cont = 0
        atual = self.__head
        while (atual):
            if atual.conteudo == conteudo:
                return self.__tamanho - cont
            atual = atual.prox
            cont += 1
        raise  PilhaException(f'Valor {conteudo} não está na pilha')

    def modificar(self, posicao:int, conteudo: Any):
        #Substitui o conteúdo do elemento na posição N
        try:
            assert posicao > 0 and posicao <= self.__tamanho
            cont = self.__tamanho
            atual = self.__head
            while cont != posicao:
                atual = atual.prox
                cont -= 1
            atual.conteudo = conteudo

        except AssertionError:
            raise PilhaException(f'Posicao inválida para a pilha atual com {self.__tamanho} elementos')

    def empilha(self, conteudo:Any):
        #Empilha um novo nó "newno"
        newno = No(conteudo)
        newno.prox = self.__head
        self.__head = newno
        self.__tamanho += 1

    def desempilha(self) -> Any:
        #Desempilha o nó head atual
        if self.estaVazia():
            raise PilhaException(f'Pilha vazia.')
        head = self.__head
        self.__head = self.__head.prox
        self.__tamanho -= 1
        return head.conteudo

    def desempilha_n(self, n) -> bool: 
        try:
            assert n > 0 and n <= self.__tamanho
            for i in range(n):
                self.desempilha()
            return True
        except AssertionError:
            return False

    def obtemBase(self) -> Any:
        cursor = self.__head
        while cursor.prox != None:
            cursor = cursor.prox
        return cursor.conteudo

    def __str__(self):
        s = '['
        #l = list()
        atual = self.__head
        while atual != None:
            #l.append(atual)
            s += f'{atual}, '
            atual = atual.prox  

        #l.reverse()
        #for i in l:
            #s += f'{i} '
        s = f'{s[:len(s)-2]}]'
        return s

    def esvazia(self):
        while not self.estaVazia():
            self.desempilha()

    def subTopo(self):
        if self.estaVazia():
            raise PilhaException(f'Pilha vazia.')
        elif self.__head.prox == None:
            raise PilhaException(f'Pilha não tem subtopo.')
        return self.__head.prox

    def inverter(self):

        if self.estaVazia():
            raise PilhaException(f'Pilha vazia.')
        
        p = Pilha()
        
        while not self.estaVazia():
            p.empilha(self.desempilha())

        self.__head = p.__head
        self.__tamanho = p.__tamanho

    def concatenar(self, pilha: object):
        t = Pilha()

        while not pilha.estaVazia():
            t.empilha(pilha.desempilha())
        while not t.estaVazia():
            self.empilha(t.desempilha())

    @classmethod
    def doubleconcatenar(cls, pilha1: object, pilha2: object):
        out = Pilha()
        t = Pilha()

        while not pilha1.estaVazia():
            t.empilha(pilha1.desempilha())
        while not t.estaVazia():
            out.empilha(t.desempilha())

        while not pilha2.estaVazia():
            t.empilha(pilha2.desempilha())
        while not t.estaVazia():
            out.empilha(t.desempilha())
            
        return out

    def existe(self, conteudo)->bool:
        """
        --MÉTODO ADICIONAL DA EQUIPE--
        Método retorna True/False sobre a existência de uma chave na pilha encadeada
        """
        atual = self.__head
        while (atual):
            if atual.conteudo == conteudo:
                return True
            atual = atual.prox
        return False