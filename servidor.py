#!/usr/bin/env python3
from modules.palavra import Palavra
from modules.tema import Tema
from modules.servidor import Server
from modules.jogador import Jogador
import socket
import threading

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

mutex = threading.Semaphore(1)
clientes = {} #Dicionário de clientes : socket
gabarito = []
inicio = False #Flag de início de uma partida
encerramento = False #Flag de encerramento (Partida cancelada, etc.)
vitoria = False #Flag de vitória

TAM_MSG = 1024 # Tamanho do bloco de mensagem
HOST = '0.0.0.0' # IP do Servidor
PORT = 40000 # Porta que o Servidor escuta

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv = (HOST, PORT)
sock.bind(serv)
sock.listen(10)

def broadcast(msg:str, dados:str = ''):
    
    global clientes

    mensagem = f'{msg} {dados}\n'.strip()
    print(mensagem)

    for cli in clientes:
        cli.send(str.encode(mensagem))

def listener():

    global mutex
    global s
    global clientes
    global gabarito
    global inicio
    global encerramento
    global vitoria

    mutex.acquire()

    while True:
        if len(clientes) > 1 and inicio == False:
            # COMEÇAR SORTEIO
            inicio = True
            s.sortearTema()
            for i in s.respostas:
                gabarito.append(str(i))
            print(f'[{s.escolhido}]{s.temaAtual}')
            broadcast('+ANO', s.temaAtual)

        elif inicio == True and len(clientes) <= 1:
            # COMEÇAR ENCERRAMENTO
            broadcast('-END')
            restart()

        elif inicio == True and len(s.respostas) == 0:
            # COMEÇAR VITÓRIA
            vitoria = True
            vencedor = ''
            maximo = 0
            for cli in clientes:
                if clientes[cli].pontuacao > maximo:
                    maximo = clientes[cli].pontuacao
                    vencedor = clientes[cli].nome

            broadcast('+WIN', vencedor)
            restart()

        mutex.release()

def restart():

    global clientes
    global gabarito
    global inicio
    global encerramento
    global vitoria

    clientes = {}
    gabarito = []
    inicio = False
    encerramento = False
    vitoria = False


def processa_msg_cliente(msg, con, cliente):

    msg = msg.decode()
    print('Cliente', cliente, 'enviou', msg)
    msg = msg.split()

    if msg[0].upper() == 'JOIN':

        nome_cli = "".join(msg[1:])
        print(f'Usuário {nome_cli} fornecido por {cliente}')

        mutex.acquire()
        if cliente not in clientes:
            try:
                clientes[con] = Jogador(nome_cli)
                con.send(str.encode('+ACK {}\n'.format(clientes[con].nome)))
            except Exception as e:
                con.send(str.encode('-ERR {}\n'.format(e)))
        else:
            con.send(str.encode('-ERR_40\n'))
        mutex.release()

    elif msg[0].upper() == 'CHUT':
        
        mutex.acquire()
        if con in clientes:
            try:
                chute = "".join(msg[1:])
                clientes[con].addTentativa(chute)
                print(f'Respostas : {gabarito}')
                print(f'<{clientes[con]}>: {chute}')
                if s.verifyPalpite(chute):
                    clientes[con].pontuar()
                    print(f'{len(s.respostas)}')
                    con.send(str.encode('+CORRECT\n'))
                else:
                    con.send(str.encode('+INCORRECT\n'))
                
            except:
                pass
        else:
            con.send(str.encode('-ERR_40\n'))
        mutex.release()
    
    elif msg[0].upper() == 'RESP':

        if inicio:
            con.send(str.encode('+OK\n'))

    elif msg[0].upper() == 'QUIT':
        con.send(str.encode('+OK\n'))
        mutex.acquire()
        if con in clientes:
            clientes.pop(con)
        mutex.release()
        return False
    else:
        con.send(str.encode('-ERR Invalid command\n'))
    return True
        
def processa_cliente(con, cliente):
    print('Cliente conectado', cliente)
    while True:
        msg = con.recv(TAM_MSG)
        if not msg or not processa_msg_cliente(msg, con, cliente): break
    con.close()
    print('Cliente desconectado', cliente)

threading.Thread(target=listener, args=()).start()

while True:
    try:
        con, cliente = sock.accept()
        threading.Thread(target=processa_cliente, args=(con, cliente,)).start()
    except: break
sock.close()













 # elif msg[0].upper() == 'LIST':
    #     lista_arq = os.listdir('.')
    #     con.send(str.encode('+OK {}\n'.format(len(lista_arq))))
    #     for nome_arq in lista_arq:
    #         if os.path.isfile(nome_arq):
    #             status_arq = os.stat(nome_arq)
    #             con.send(str.encode('arq: {} - {:.1f}KB\n'.
    #                 format(nome_arq, status_arq.st_size/1024)))
    #         elif os.path.isdir(nome_arq):
    #             con.send(str.encode('dir: {}\n'.format(nome_arq)))
    #         else:
    #             con.send(str.encode('esp: {}\n'.format(nome_arq)))
       
    # elif msg[0].upper() == 'CWD':
    #     caminho_solicitado = " ".join(msg[1:])
    #     print('Novo Diretório: ', caminho_solicitado)
    #     try:
    #         os.chdir(caminho_solicitado)
    #         con.send(str.encode('+OK\n'))
    #     except Exception as e:
    #         con.send(str.encode('-ERR Invalid command\n'))