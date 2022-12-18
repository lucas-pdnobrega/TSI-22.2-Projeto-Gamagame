class GamaException(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)

class Palavra:
    def __init__(self, peso:int, valor:str):
        try:
            assert peso > 0 and valor != ''
            self.__peso = peso
            self.__valor = valor
        except AssertionError:
            raise GamaException('Entradas (peso e/ou valor) inválidas!')

    def __str__(self):
        return f'{self.__valor} : {self.__peso}'

    def __lt__(self, other) -> bool:
        return self.__peso < other.__peso 

    def __le__(self, other) -> bool:
        return self.__peso <= other.__peso 

    def __eq__(self, other) -> bool:
        return self.__peso == other.__peso 

    def __ne__(self, other) -> bool:
        return self.__peso != other.__peso 

    def __gt__(self, other) -> bool:
        return self.__peso > other.__peso 

    def __ge__(self, other) -> bool:
        return self.__peso >= other.__peso 

    @property
    def peso(self) -> int:
        return self.__peso

    @property
    def valor(self) -> int:
        return self.__valor

    @peso.setter
    def peso(self, peso:int) -> int:
        try:
            assert peso > 0
            self.__peso = peso
        except AssertionError:
            raise GamaException('Entradas (peso) inválidas!')

    @valor.setter
    def valor(self, valor:int) -> int:
        try:
            assert valor != ''
            self.__valor = valor
        except AssertionError:
            raise GamaException('Entradas (valor) inválidas!')