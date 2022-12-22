#!/usr/bin/env python3
from modules.palavra import Palavra
from modules.tema import Tema
from modules.jogador import Jogador
from modules.servidor import Server, GamaException
import socket
import threading
import sys

'''
Definição de recursos para alimentação da aplicação
'''
#Lista de objetos Palavra 'comidas'
comidas = [Palavra(12, 'Samgyetang'),
Palavra(4, 'Macarronada'), 
Palavra(3, 'Feijoada'),
Palavra(2, 'Lasanha'),
Palavra(1, 'Pizza'),
Palavra(12, 'Shakshuka'),
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
Palavra(6, 'Pavê'),
Palavra(9, 'Risoto'),
Palavra(4, 'Espetinho'),
Palavra(10, 'Strogonoff'),
Palavra(2, 'Coxinha'),
Palavra(6, 'Panqueca'),
Palavra(3, 'Pastel'),
Palavra(2, 'Pão'),
Palavra(7, 'Sopa')]

#Lista de objetos Palavra 'paises_da_copa_2022'
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

#Inserção das listas de palavras nos seus temas correspondentes
comidas = Tema('Comidas', comidas)
paises = Tema('Paises da Copa 2022', paises_da_copa_2022)
s = Server([comidas, paises]) # Classe responsável por administrar os dados do servidor

mutex = threading.Semaphore(1) #Semáforo para exclusão mútua
clientes = {} #Dicionário de clientes : socket
respostas = [] #Lista de respostas em str ao invés de objetos Palavra() para conveniência

'''
Função para extrair máximo de jogadores por partida, se aplicável
'''
if len(sys.argv) > 1:
    try:
        maxjogadores = int(sys.argv[1])
    except:
        raise GamaException('Número de participantes fornecido é inválido!')
else:
    maxjogadores = 2

inicio = False #Flag de início de uma partida
encerramento = False #Flag de encerramento (Partida cancelada)
vitoria = False #Flag de vitória

TAM_MSG = 1024 # Tamanho do bloco de mensagem
HOST = '0.0.0.0' # IP do Servidor
PORT = 40000 # Porta que o Servidor escuta

'''
Inicialização da porta do servidor
''' 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv = (HOST, PORT)
sock.bind(serv)
sock.listen(10)


def broadcast(msg:str, dados:str = '', adendo:any = ''):
    '''
    Função para realização do broadcast para todos os jogadores registrados na partida atual
    '''
    global clientes

    mensagem = f'{msg} {dados} {adendo}\n'.strip()
    print(mensagem)

    for cli in clientes:
        cli.send(str.encode(mensagem))

def listener():
    '''
    Função thread para averiguação do estado atual do servidor e da partida
    '''
    global mutex
    global s
    global clientes
    global respostas
    global inicio
    global encerramento
    global vitoria
    global maxjogadores

    while True:
        mutex.acquire()
        if len(clientes) == maxjogadores and inicio == False:
            # INICIALIZAR O SORTEIO DO TEMA
            inicio = True
            s.sortearTema()

            #Preenchimento da lista de respostas em str para logging
            res = s.respostas
            for r in res:
                respostas.append(str(r))
            print(f'Tema Atual : {s.temaAtual}')
            broadcast('+ANO', s.temaAtual)

        elif inicio == True and len(clientes) < maxjogadores:
            # INICIAR BROADCAST DE ENCERRAMENTO
            broadcast('-END')
            restart()

        elif inicio == True and len(s.respostas) == 0:
            # INICIAR BROADCAST DE VITÓRIA
            vitoria = True
            vencedor = ''
            maximo = 0

            #PESQUISA LINEAR PELO VENCEDOR (Prioridade aos primeiros da lista)
            for cli in clientes:
                if clientes[cli].pontuacao > maximo:
                    maximo = clientes[cli].pontuacao
                    vencedor = clientes[cli].nome

            broadcast('+WIN', vencedor, maximo)
            restart()

        mutex.release()

def restart():
    '''
    Função para reinicializar todos as propriedades globais do servidor
    '''
    print('Reinicialização...')
    global mutex
    global clientes
    global inicio
    global encerramento
    global vitoria
    global respostas

    clientes = {}
    respostas = []
    inicio = False
    encerramento = False
    vitoria = False


def processa_msg_cliente(msg, con, cliente):

    msg = msg.decode()
    print('Cliente', cliente, 'enviou', msg)
    msg = msg.split()

    if msg[0].upper() == 'JOIN':

        if not inicio:
            nome_cli = "".join(msg[1:])

            if len(nome_cli) > 1:
                print(f'Usuário {nome_cli} fornecido por {cliente}')

                mutex.acquire()
                if con not in clientes and nome_cli not in clientes.values():
                    try:
                        clientes[con] = Jogador(nome_cli) #Inserção da socket atual como chave e valor correspondente objeto Jogador
                        con.send(str.encode('+ACK {}\n'.format(clientes[con].nome)))
                    except Exception as e:
                        con.send(str.encode('-ERR {}\n'.format(e)))
                else:
                    con.send(str.encode('-ERR_41\n')) #Usuário já participa da partida
                mutex.release()
            else:
                con.send(str.encode('-ERR_43\n')) #Entrada Inválida
        else:
            con.send(str.encode('-ERR_42\n')) #Partida em Andamento

    elif msg[0].upper() == 'CHUT':
        
        mutex.acquire()
        if inicio:
            if con in clientes:
                try:
                    chute = "".join(msg[1:])
                    if len(chute) > 0:
                        clientes[con].addTentativa(chute)
                        print(f'<{clientes[con]}>: {chute}')

                        #Varrer as respostas pelo peso correspondente   
                        peso = 0
                        for res in s.respostas:
                            if chute.lower() == res.termo.lower():
                                peso = res.peso

                        if s.verifyPalpite(chute):
                            clientes[con].pontuar(peso)
                            con.send(str.encode('+CORRECT\n')) #Palpite Correto
                        else:
                            con.send(str.encode('+INCORRECT\n')) #Palpite Incorreto
                        print(f'Respostas : {respostas}')
                    else:
                        con.send(str.encode('-ERR_43\n')) #Entrada Inválida
                except:
                    pass
            else:
                con.send(str.encode('-ERR_40\n')) #Usuário não participa da partida
        else:
            con.send(str.encode('-ERR_44\n'))
        mutex.release()

    elif msg[0].upper() == 'QUIT':
        mutex.acquire()
        if con in clientes:
            clientes.pop(con)
        mutex.release()
        return False
    else:
        con.send(str.encode('-ERR_45\n'))
    return True
        
def processa_cliente(con, cliente):
    '''
    Função para entrada de cliente no servidor
    '''
    print('Cliente conectado', cliente)
    while True:
        msg = con.recv(TAM_MSG)
        if not msg or not processa_msg_cliente(msg, con, cliente): break
    con.close()
    print('Cliente desconectado', cliente)

#Inicialização do daemon de estado da partida
threading.Thread(target=listener, args=()).start()

while True:
    try:
        con, cliente = sock.accept()
        threading.Thread(target=processa_cliente, args=(con, cliente,)).start()
    except: break
sock.close()