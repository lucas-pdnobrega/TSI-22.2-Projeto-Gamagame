#!/usr/bin/env python3
import socket
import sys
import threading

TAM_MSG = 1024 # Tamanho do bloco de mensagem
HOST = '127.0.0.1' # IP do Servidor
PORT = 40000 # Porta que o Servidor escuta
encerramento = False

def decode_cmd_usr(cmd_usr):
    if encerramento:
        return ''.join('quit')
    cmd_map = {
        'join': 'join',
        'chute' : 'chut',
        'respostas': 'resp',
        'quit' : 'quit',
        'exit': 'quit'
    }
    tokens = cmd_usr.split()
    if tokens[0].lower() in cmd_map:
        tokens[0] = cmd_map[tokens[0].lower()]
        return " ".join(tokens)
    else:
        return False

if len(sys.argv) > 1:
    HOST = sys.argv[1]

def processa_servidor():

    global encerramento

    while True:
        if encerramento:
            break

        dados = sock.recv(TAM_MSG)
        if not dados: break
        msg_status = dados.decode().split('\n')[0]
        sys.stdout.write(f'{msg_status}\n')
        sys.stdout.flush()

        args = msg_status.split()

        if args[0] == '-END':
            print('Partida cancelada por problemas de conexão.\n')
            encerramento = True

        elif args[0] == '+ACK':
            print(f'Conexão aceita pelo servidor, usuário {args[1]}')

        elif args[0] == '+CORRECT':
            print(f'O palpite estava correto!')

        elif args[0] == '+INCORRECT':
            print(f'O palpite estava incorreto...')

        elif args[0] == '+WIN':
            print(f'Partida concluída! {args[1]} ganhou\n')
            encerramento = True

        elif args[0] == '+ANO':
            print(f'O tema sorteado da vez é {args[1]}!\n')

        elif args[0] == '-ERR_40':
            print(f'Erro 40 - Usuário não participante da partida')

        elif args[0] == '-ERR_41':
            print(f'Erro 41 - Usuário já participante na partida')

        elif args[0] == '-ERR_42':
            print(f'Erro 42 - Partida em andamento')

        elif args[0] == '-ERR_43':
            print(f'Erro 43 - Entrada inválida')


print('Servidor:', HOST+':'+str(PORT))

serv = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(serv)

print('Para encerrar use EXIT, CTRL+D ou CTRL+C\n')

t = threading.Thread(target=processa_servidor, args=())
t.daemon = True
t.start()

while True:

    if encerramento:
            break
    try:
        cmd_usr = input()
    except:
        cmd_usr = 'EXIT'
    cmd = decode_cmd_usr(cmd_usr)
    if not cmd:
        print('Comando indefinido:', cmd_usr)
    else:
        sock.send(str.encode(cmd))
        cmd = cmd.split()
        cmd[0] = cmd[0].upper()

        if cmd[0] == 'QUIT':
            break

        elif cmd[0] == 'JOIN':
            continue

        elif cmd[0] == 'CHUT':
            continue

        elif cmd[0] == 'RESP':
            continue

sock.close()






# elif cmd[0] == 'LIST':
        #     num_arquivos = int(msg_status.split()[1])
        #     dados = dados.decode()
        #     while True:
        #         arquivos = dados.split('\n')
        #         residual = arquivos[-1] #último sem \n fica para próxima
        #         for arq in arquivos[:-1]:
        #             print(arq)
        #             num_arquivos -= 1
        #         if num_arquivos == 0: break
        #         dados = sock.recv(TAM_MSG)
        #         if not dados: break
        #         dados = residual + dados.decode()
        # elif cmd[0] == 'GET':
        #     nome_arq = " ".join(cmd[1:])
        #     print('Recebendo:', nome_arq)
        #     arq = open(nome_arq, "wb")
        #     tam_arquivo = int(msg_status.split()[1])
        #     while True:
        #         arq.write(dados)
        #         tam_arquivo -= len(dados)
        #         if tam_arquivo == 0: break
        #         dados = sock.recv(TAM_MSG)
        #         if not dados: break
        #     arq.close()