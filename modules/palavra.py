class GamaException(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)

class Palavra:
    def __init__(self, peso:int, valor:str):
        try:
            assert peso > 0, valor != ''
            self.__peso = peso
            self.__valor = valor
        except AssertionError:
            raise GamaException('Entradas (peso e/ou valor) inválidas!')

    def __str__(self):
        return f'{self.__valor} : {self.__peso}'

    def __lt__(self, other) -> bool:
        return True if self.__peso < other.__peso else False

    def __le__(self, other) -> bool:
        return True if self.__peso <= other.__peso else False

    def __eq__(self, other) -> bool:
        return True if self.__peso == other.__peso else False

    def __ne__(self, other) -> bool:
        return True if self.__peso != other.__peso else False

    def __gt__(self, other) -> bool:
        return True if self.__peso > other.__peso else False

    def __ge__(self, other) -> bool:
        return True if self.__peso >= other.__peso else False

    @property
    def peso(self) -> int:
        return self.__peso

    @property
    def valor(self) -> int:
        return self.__valor

    @peso.setter
    def peso(self, peso:int) -> int:
        return self.__peso

    @valor.setter
    def valor(self, valor:int) -> int:
        return self.__valor