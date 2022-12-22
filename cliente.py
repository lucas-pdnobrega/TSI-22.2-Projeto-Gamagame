#!/usr/bin/env python3
import socket
import sys
import threading
from modules.utils import loading

TAM_MSG = 1024 # Tamanho do bloco de mensagem
HOST = '127.0.0.1' # IP do Servidor
PORT = 40000 # Porta que o Servidor escuta
mutex = threading.Semaphore(1) #Semáforo para exclusão mútua
encerramento = False # Flag de encerramento do cliente
participa = False # Flag de se o cliente participa de uma partida

#Função decodificar comandos do usuário
def decode_cmd_usr(cmd_usr):
    cmd_map = {
        'join': 'join',
        'chute' : 'chut',
        'quit' : 'quit'
    }
    tokens = cmd_usr.split()
    
    if encerramento:
        return ''.join('quit')
    elif tokens[0].lower() in cmd_map:
        tokens[0] = cmd_map[tokens[0].lower()]
        return " ".join(tokens)
    elif participa == True:
        return f'chut {cmd_usr}'
    else:
        return False

if len(sys.argv) > 1:
    HOST = sys.argv[1]

def processa_servidor():
    '''
    Função thread para processar respostas do servidor
    '''
    global encerramento
    global participa

    while True:

        try:

            if encerramento: break

            dados = sock.recv(TAM_MSG)
            if not dados: break
            msg_status = dados.decode().split('\n')[0]

            sys.stdout.flush()
            args = msg_status.split()

            if args[0] == '+ACK':
                print(f'Conexão aceita pelo servidor, usuário {args[1]}\n')
                mutex.acquire()
                participa = True
                mutex.release()

            elif args[0] == '+CORRECT':
                print('\033[1;36m O palpite estava correto!\033[1;0m\n')

            elif args[0] == '+INCORRECT':
                print('\033[1;31m O palpite estava incorreto...\033[1;0m\n')

            elif args[0] == '+WIN':
                print(f'\n\033[1;33m Partida concluída! {args[1]} ganhou com {args[2]} pontos!\033[0m\n')
                mutex.acquire()
                encerramento = True
                mutex.release()
                break

            elif args[0] == '+ANO':
                print(f'O tema sorteado da vez é {args[1]}!\n')

            elif args[0] == '-END':
                print('Partida cancelada por problemas de conexão.\n')
                mutex.acquire()
                encerramento = True
                mutex.release()
                break

            elif args[0] == '-ERR_40':
                print(f'Erro 40 - Usuário não participante da partida\n')

            elif args[0] == '-ERR_41':
                print(f'Erro 41 - Endereço já está cadastrado da partida\n')

            elif args[0] == '-ERR_42':
                print(f'Erro 42 - Partida em andamento\n')

            elif args[0] == '-ERR_43':
                print(f'Erro 43 - Entrada inválida\n')

            elif args[0] == '-ERR_44':
                print(f'Erro 44 - Partida não iniciada\n')

            else:
                print(f'Erro desconhecido - {args[1]}\n')
        except: break

serv = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(serv)

loading(0.3, 2, 1) #Exibir título do projeto

print('Para entrar em uma partida, utilize join seguido de seu usuário\nPara encerrar use QUIT, CTRL+D ou CTRL+C\n')

#Inicialização do Thread de processamento de respostas do servidor
t = threading.Thread(target=processa_servidor, args=())
t.start()

while True:

    if encerramento:
        break
    try:
        cmd_usr = input()
    except:
        cmd_usr = 'QUIT'
    cmd = decode_cmd_usr(cmd_usr)

    if not cmd:
        print('Comando indefinido:', cmd_usr)
    else:
        sock.send(str.encode(cmd))
        cmd = cmd.split()
        cmd[0] = cmd[0].upper()

        if cmd[0] == 'QUIT':
            encerramento = True
            break

sock.close()