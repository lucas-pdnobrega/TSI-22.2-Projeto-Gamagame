#!/usr/bin/env python3
import socket
import os
import threading

TAM_MSG = 1024 # Tamanho do bloco de mensagem
HOST = '0.0.0.0' # IP do Servidor
PORT = 40000 # Porta que o Servidor escuta

mutex = threading.Semaphore(1)
clientes = {}
# socket : nome

def broadCast(msg, atributos, clientes):
    for cli in clientes:
        cli.send(str.encode('+JANO\n '))
        # cli.send(str.encode('+JANO {}\n'.format(clientes[con])))

def processa_msg_cliente(msg, con, cliente):

    global clientes
    global mutex

    msg = msg.decode()
    print('Cliente', cliente, 'enviou', msg)
    msg = msg.split()
    
    if msg[0].upper() == 'JOIN':
        nome_cli = "".join(msg[1:])
        print(f'Usuário {nome_cli} fornecido por {cliente}')
        mutex.acquire()
        if con not in clientes:
            try:
                clientes[con] = nome_cli
                con.send(str.encode('+OK {}\n'.format(clientes[con])))
                for cli in clientes:
                    print(cli)
                    cli.send(str.encode('+JANO {}\n'.format(clientes[con])))
            except Exception as e:
                con.send(str.encode('-ERR {}\n'.format(e)))
        else:
            con.send(str.encode('-ERR 40\n'))
        mutex.release()
    
    elif msg[0].upper() == 'HEY':
        con.send(str.encode('+HEY\n'))

    elif msg[0].upper() == 'LIST':
        lista_arq = os.listdir('.')
        con.send(str.encode('+OK {}\n'.format(len(lista_arq))))
        for nome_arq in lista_arq:
            if os.path.isfile(nome_arq):
                status_arq = os.stat(nome_arq)
                con.send(str.encode('arq: {} - {:.1f}KB\n'.
                    format(nome_arq, status_arq.st_size/1024)))
            elif os.path.isdir(nome_arq):
                con.send(str.encode('dir: {}\n'.format(nome_arq)))
            else:
                con.send(str.encode('esp: {}\n'.format(nome_arq)))
    
    elif msg[0].upper() == 'CWD':
        caminho_solicitado = " ".join(msg[1:])
        print('Novo Diretório: ', caminho_solicitado)
        try:
            os.chdir(caminho_solicitado)
            con.send(str.encode('+OK\n'))
        except Exception as e:
            con.send(str.encode('-ERR Invalid command\n'))


    elif msg[0].upper() == 'QUIT':
        con.send(str.encode('+OK\n'))
        mutex.acquire()
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
    mutex.acquire()
    clientes.pop(con)
    mutex.release()
    print('Cliente desconectado', cliente)
    
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv = (HOST, PORT)
sock.bind(serv)
sock.listen(10)
while True:
    try:
        con, cliente = sock.accept()
        threading.Thread(target=processa_cliente, args=(con, cliente,)).start()
    except: break
    #processa_cliente(con, cliente)
sock.close()

# while True: # checagem apenas no login do cliente
#     try:
#         con, cliente = sock.accept()  # con -> socket retornado pelo accept
#     except: break
#     threading.Thread(target=processar_cliente, args=(con, cliente,)).start()
sock.close()