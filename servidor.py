from arvoreBinaria import ArvoreBinaria
import socket
import threading

TAM_MSG = 1024
HOST = '0.0.0.0'
PORT = '5000'

partida = ArvoreBinaria()

def processar_cliente(con, cliente):  # con -> socket de conexão; cliente -> IP: PORT do parceiro
    print('Conectado com', cliente)
    while True:
        msg = con.recv(1024)
        if not msg: break
        print(cliente, 'mensagem:', msg.decode())
        con.send(msg)
    print('Desconectando do cliente', cliente)
    con.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv = (HOST, PORT)
sock.bind(serv)
sock.listen(50)
while True:
    try:
        con, cliente = sock.accept()  # con -> socket retornado pelo accept
    except: break
    threading.Thread(target=processar_cliente, args=(con, cliente,)).start()
sock.close()
