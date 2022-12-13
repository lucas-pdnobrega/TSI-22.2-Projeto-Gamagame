#!/usr/bin/env python3

from pilhaEncadeada import Pilha
import socket
import sys

HOST = '127.0.0.1'
PORT = 5000

# if len(sys.argv) > 1:  # se passarmos um IP como argumento (exemplo: ./cliente.py 200.129.2.1)
#     HOST = sys.argv[1]

nome_jogador = input('Insira o seu nome de usuário : ')

servidor = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(servidor)

sock.send(str.encode(nome_jogador))
retorno = sock.recv(1024)

if retorno:
    retorno = retorno.decode()
    print(f"{retorno} entrou no servidor")
else:
    print("Não há partidas")

while True:
    try:
        msg = 'RYLP > '
        msg +=  input('\nRYLP (Ctrl + D para encerrar) > ') # 'Oi Mundo Socket!' -> mensagem de teste
        print(msg)
    except EOFError: break
    sock.send(str.encode(msg))  # encode vai retornar um vetor de bytes, já que o send espera receber um vetor de bytes
    msg = sock.recv(1024)
    if msg:
        msg = msg.decode()
        print('Recebi:', msg)
sock.close()

# tentativas = Pilha()
# palavras = ['batata', 'macaxeira', 'inhame']

# while len(palavras) != 0:  
#     print(f's {len(palavras)} {palavras}')    
#     print(tentativas)

#     # Extrair somente tentativa única
#     while True:
        
#         tentativa = input('Tentativa : ').lower().strip()

#         #SEMÁFORO?
#         if not tentativas.existe(tentativa):
#             break
#         print('Tentativa repetida, tente novamente!')
    
#     # Verificar se tentativa é correta
#     tentativas.empilha(tentativa)

# print('FIM DO PROGRAMA')