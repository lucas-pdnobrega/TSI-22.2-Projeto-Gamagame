from modules.palavra import Palavra
from modules.tema import Tema

palavras = [Palavra(1, 'Dó'), Palavra(2, 'Ré'), Palavra(3, 'Mi'), Palavra(4, 'Fá'), Palavra(5, 'Sol'), Palavra(6, 'Lá'), Palavra(7, 'Si'), Palavra(8, 'Dó^'), Palavra(9, 'KLFJlsjdflkjfsgldnfkjg')]
tema = Tema('Notas', palavras)
print(f'Tema = {tema}')
p = tema.avlPalavras
for i in p:
    print(i)

tema.addPalavra(3, 'Omnitrix')

sorteadas1 = tema.sortearPalavras(3)
for i in sorteadas1:
    print(i, end='; ')
print('',end = '\n')
sorteadas2 = tema.sortearPalavras(5)
for i in sorteadas2:
    print(i, end='; ')
print('',end = '\n')
sorteadas3 = tema.sortearPalavras(6)
for i in sorteadas3:
    print(i, end='; ')