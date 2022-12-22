from time import sleep
import os
import sys
# Função para exibir o loading e título do projeto
def loading(t, vezes, clear):
    done = False
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    while done == False:
        for repetir in range(vezes):
            sys.stdout.write('\rCarregando (     )')
            sleep(t)
            sys.stdout.write('\rCarregando (.    )')
            sleep(t)
            sys.stdout.write('\rCarregando (. .  )')
            sleep(t)
            sys.stdout.write('\rCarregando (. . .)')
            sleep(t)
        done = True
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.write(f'''\n\033[1;33m
    ─▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄
    █░░░█░░░░░░░░░░▄▄░██░█
    █░▀▀█▀▀░▄▀░▄▀░░▀▀░▄▄░█
    █░░░▀░░░▄▄▄▄▄░░██░▀▀░█
    ─▀▄▄▄▄▄▀─────▀▄▄▄▄▄▄▀

    Projeto GAMAGAME - ADIVINHA PALAVRAS

    Integrantes :
       - Lucas Palmeira
       - Renato Melo
       - Yago César
    \033[0m\n''')
    sleep(5)
    # Limpar o terminal
    if clear == 1:
        os.system('cls' if os.name == 'nt' else 'clear')