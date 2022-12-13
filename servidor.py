#!/usr/bin/env python3

from arvoreBinaria import ArvoreBinaria
import socket
import threading

TAM_MSG = 1024
HOST = '0.0.0.0'
PORT = 5000

partida = ArvoreBinaria()

################################
## MÉTODOS DO NOSSO PROTOCOLO ##
################################

# palpite
# ver tentativa
# ver respostas
# sair

#temas = arvoreBinaria()
#

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv = (HOST, PORT)
sock.bind(serv)
sock.listen(16)

palavras = ['batata', 'macaxeira', 'inhame']
clientes = []

def processar_cliente(con, cliente):  # con -> socket de conexão; cliente -> IP: PORT do parceiro
    print('Conectado com', cliente)
    # O RESTO
    while True:
        msg = con.recv(TAM_MSG)
        if not msg: break
        if len(msg.decode().split('RYLP >')) > 1:
            print(cliente, 'mensagem:', msg.decode())
        else:
            clientes.append(msg.decode())
            print(clientes)
        con.send(msg)
    print('Desconectando do cliente', cliente)
    con.close()


while True:
    try:
        con, cliente = sock.accept()  # con -> socket retornado pelo accept
    except EOFError: break
    threading.Thread(target=processar_cliente, args=(con, cliente,)).start()
sock.close()

#     #SEMÀFOROOOOO
#     mutex = threading.Semaphore(1)

#     mutex.acquire()
#     if msg.decode() in palavras:
#         for i in range(len(palavras)):
#             if palavras[i] == msg:
#                 palavras.pop(i)
#                 break
#         con.send(str(f'O palpite da palavra {tentativa} de PESSOA estava certo!').encode())
#     else:
#         con.send(str(f'O palpite da palavra {tentativa} de PESSOA estava errado...').encode())
#     mutex.release()