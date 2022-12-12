from pilhaEncadeada import Pilha

tentativas = Pilha()
palavras = ['batata', 'macaxeira', 'inhame']

while len(palavras) != 0:  
    print(f's {len(palavras)} {palavras}')    
    print(tentativas)

    # Extrair somente tentativa única
    while True:
        
        tentativa = input('Tentativa : ').lower().strip()

        #SEMÁFORO?
        if not tentativas.existe(tentativa):
            break
        print('Tentativa repetida, tente novamente!')
    
    # Verificar se tentativa é correta
    if tentativa in palavras:
        for i in range(len(palavras)):
            if palavras[i] == tentativa:
                palavras.pop(i)
                break
        print(f'O palpite da palavra {tentativa} de PESSOA estava certo!')
    else:
        print(f'O palpite da palavra {tentativa} de PESSOA estava errado...')
    tentativas.empilha(tentativa)

print('FIM DO PROGRAMA')