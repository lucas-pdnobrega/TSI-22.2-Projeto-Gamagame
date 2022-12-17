from modules.palavra import Palavra
from modules.tema import Tema

palavras = [Palavra(1, 'Dó'), Palavra(2, 'Ré'), Palavra(3, 'Mi'), Palavra(4, 'Fá'), Palavra(5, 'Sol'), Palavra(6, 'Lá'), Palavra(7, 'Si'), Palavra(8, 'Dó^')]
tema = Tema('', 3, palavras)
print(f'Tema = {tema}')
p = tema.avlPalavras
for i in p:
    print(i)