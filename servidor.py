#!/usr/bin/env python3

from arvoreBinaria import ArvoreBinaria
import socket
import threading


TAM_MSG = 1024
HOST = '0.0.0.0'
PORT = 5000

partida = ArvoreBinaria()
mutex = threading.Semaphore(1)

################################
## MÉTODOS DO NOSSO PROTOCOLO ##
################################

# palpite
# ver tentativa
# ver respostas
# sair

#temas = arvoreBinaria()
#

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv = (HOST, PORT)
sock.bind(serv)
sock.listen(4)

palavras = ['batata', 'macaxeira', 'inhame']
clientes = {
	# user: socket -> usar aquele socket con (aquele que volta do accept)
}  # tem que fazer parte do mutex
# percorrer a lista de clientes e informar a cada um quem ganhou

def processar_cliente(con, cliente):  # con -> socket de conexão; cliente -> IP: PORT do parceiro
    print('Conectado com', cliente)
    # O RESTO
    while True:  # while partida esta rolando
        msg = con.recv(TAM_MSG)
        if not msg: break

        mensagem = msg.decode().split('RYLP > ')
        
        if len(mensagem) > 1:
            tentativa = mensagem[1]
            veracidade = False
            
            #if mensagem[1].upper() == 'nome':
                #con.send(str(f'Seu nome é: {nome_jogador} ').encode())
            mutex.acquire()            
            for i in range(len(palavras)):
                if palavras[i] == tentativa:
                    veracidade = True
                    palavras.pop(i)  # verificar se há palavras depois do pop
					# notificar todos os jogadores do fim do jogo -> 1. identificar o ganhador (maior potuação)
					# except
                    print(palavras)
                    con.send(str(f'O palpite da palavra {tentativa} de PESSOA estava certo!').encode())  # NÃO MANDAR ESSAS STRINGS
					# SERVIDOR SIMPLIFICADO -> mandar um 'OK' ou algo do tipo
                    break
            mutex.release()
            if not veracidade:
                con.send(str(f'O palpite da palavra {tentativa} de PESSOA estava errado...').encode())

            print(cliente, 'mensagem:', msg.decode())
        else:
			mutex.acquire()
			clientes.append(msg.decode())
			print(clientes)
			mutex.release()
            con.send(msg)
    print('Desconectando do cliente', cliente)
    con.close()

# mandar a msg fim de jogo e fechar o socket para cada conexão

while len(palavras) > 0: # checagem apenas no login do cliente
    try:
        con, cliente = sock.accept()  # con -> socket retornado pelo accept
    except: break
    threading.Thread(target=processar_cliente, args=(con, cliente,)).start()

#up do semáforo - mutex?
# semáforo que, quando estiver up, matará todas as outras threads
sock.close()


print('FIM DO PROGRAMA')












'''
#!/usr/bin/env python3
import socket
import os
import threading
TAM_MSG = 1024 # Tamanho do bloco de mensagem
HOST = '0.0.0.0' # IP do Servidor
PORT = 40000 # Porta que o Servidor escuta
def processa_msg_cliente(msg, con, cliente):
	msg = msg.decode()
	print('Cliente', cliente, 'enviou', msg)
	msg = msg.split()
	if msg[0].upper() == 'GET':
		nome_arq = " ".join(msg[1:])
		print('Arquivo solicitado:', nome_arq)
		try:
			status_arq = os.stat(nome_arq)
			con.send(str.encode('+OK {}\n'.format(status_arq.st_size)))
			arq = open(nome_arq, "rb")
			while True:
				dados = arq.read(TAM_MSG)
				if not dados: break
				con.send(dados)
		except Exception as e:
			con.send(str.encode('-ERR {}\n'.format(e)))
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
	
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv = (HOST, PORT)
sock.bind(serv)
sock.listen(50)
while True:
	try:
		con, cliente = sock.accept()
	except: break
	#processa_cliente(con, cliente)
	pid = os.fork()
	if pid == 0:
		sock.close()
		processa_cliente(con,cliente)
		break
	else:
		con.close()
sock.close()



'''