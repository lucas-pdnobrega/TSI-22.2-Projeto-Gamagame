<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white%22/%3E" />

# Projeto-Gamagame

## &nbsp; Implementação cliente-servidor em Python do jogo Gamagame

    A aplicação Gamagame é um jogo baseado em um chat onde haverá uma
    lista dividido em categorias (temas). Para cada categoria haverá 
    5 itens (palavras) sorteados e, no início do jogo, o chat será 
    informado qual a categoria foi sorteada e os participantes do chat
    tentarão acertar os itens sorteados. Clientes mandam suas respostas
    (tentativas) para o servidor e este administra a partida. Quando a 
    resposta (tentativa) informada pelo usuário for uma das que foram 
    sorteadas, aquele participante que respondeu corretamente o peso da palavra 
    como pontuação, o peso é baseado na dificuldade.


## &nbsp; Integrantes
  - Lucas Palmeira Dantas da Nobrega(20221370016)
  - Renato Bezerra de Melo(20221370002)
  - Yago César de Nascimento Aguiar(20221370018)


## &nbsp; Estruturas de Dados utilizadas
  - Árvore AVL na classe Tema
  - Pilha Encadeada na classe Jogador


## &nbsp; Requisições do Protocolo de Aplicação RYLP
  - JOIN : Requisição de Cliente para entrar numa partida do Servidor.
  - CHUTE : Requisição de Cliente para encaminhar um palpite de palavra ao Servidor.
  - QUIT : Notificação para saída do Cliente da partida.

## &nbsp; Respostas do Protocolo de Aplicação RYLP
  - +ACK [args] : Utilizado pelo servidor para ...
  - +CORRECT : Utilizado pelo servidor para notificar que o palpite de um dado usuário foi correto.
  - +INCORRECT : Utilizado pelo servidor para notificar que o palpite de um dado usuário foi incorreto.
  - -ERR [args] : Utilizado para o servidor realizar a notificação personalizada de erro para o cliente.
  - -ERR_40 : Utilizado quando usuário não participante de uma dada partida tenta fazer palpite nela.
  - -ERR_41 : Utilizado para notificar que o endereço do usuário já está cadastrado na partida.
  - -ERR_42 : Utilizado para notificar um usuário de que não é possível entrar por conta de uma partida em andamento.
  - -ERR_43 : Utilizado para notificar um usuário de que a entrada fornecida não é válida.
  - -ERR_44 : Utilizado para informar os usuários que a partida não foi iniciada.