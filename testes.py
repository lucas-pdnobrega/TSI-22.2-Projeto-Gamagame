from modules.palavra import Palavra
from modules.tema import Tema
from modules.servidor import Server

comidas = [Palavra(10, 'Samgyetang'),
Palavra(4, 'Macarronada'), 
Palavra(3, 'Feijoada'),
Palavra(2, 'Lasanha'),
Palavra(1, 'Pizza'),
Palavra(10, 'Shakshuka'),
Palavra(5, 'Torta'), 
Palavra(4, 'Bolo'), 
Palavra(6, 'Paçoca'),
Palavra(10, 'Brusqueta'),
Palavra(7, 'Tapioca'), 
Palavra(2, 'Salada'),
Palavra(2, 'Farofa'),
Palavra(1, 'Salpicão'),
Palavra(1, 'Arroz'),
Palavra(3, 'Peru'), 
Palavra(3, 'Frango'), 
Palavra(6, 'Pavê')]

paises_da_copa_2022 = [Palavra(3,'Alemanha'),
Palavra(1,'Argentina'),
Palavra(8,'Austrália'),
Palavra(4,'Bélgica'),
Palavra(1,'Brasil'),
Palavra(11,'Camarões'),
Palavra(10,'Canadá'),
Palavra(8,'Catar'),
Palavra(11,'Coreia'),
Palavra(4,'Croácia'),
Palavra(6,'Dinamarca'),
Palavra(6,'Equador'),
Palavra(2,'Espanha'),
Palavra(3,'França'),
Palavra(7,'Gana'),
Palavra(3,'Holanda'),
Palavra(2,'Inglaterra'),
Palavra(8,'Irã'),
Palavra(8,'Japão'),
Palavra(9,'Marrocos'),
Palavra(9,'México'),
Palavra(10,'Gales'),
Palavra(4,'Polônia'),
Palavra(7,'Portugal'),
Palavra(5,'Senegal'),
Palavra(5,'Sérvia'),
Palavra(6,'Suíça'),
Palavra(6,'Tunísia'),
Palavra(7,'Uruguai')]

comidas = Tema('Comidas', comidas)
paises = Tema('Paises da Copa 2022', paises_da_copa_2022)

s = Server([comidas, paises])

s.sortearTema()
print(f'[{s.escolhido}]{s.temaAtual}')
for i in s.respostas:
    print(i, end="; ")
print()
while len(s.respostas) > 0:
    print(f'Faltam {len(s.respostas)}!')
    print(s.verifyPalpite(input()))