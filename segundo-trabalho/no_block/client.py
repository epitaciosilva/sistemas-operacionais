
import sys
import time
import json
import math
import random
import pygame
import socket
import pickle
import select
import copy
import tkinter as tk
from tkinter import messagebox
from snake import snake, cube, randomSnack, redrawWindow

def positions(obj):
    return list(map(lambda x: x.pos, obj))

def main():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65433  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        width = 500
        rows = 20
        
        cobra = snake((255, 0, 200), (10, 10))  # cria snake do cliente
        s.connect((HOST, PORT))
        s.sendall(pickle.dumps(cobra))  # enviando cobra do cliente pro servidor
        data = s.recv(1024)  # recebendo dados do servidor
        client_ip = pickle.loads(data)  # recebendo outras cobras do servidor

        s.sendall(pickle.dumps(cobra))  # enviando cobra do cliente pro servidor
        data = s.recv(1024)  # recebendo dados do servidor
        snakes = pickle.loads(data)

        win = pygame.display.set_mode((width, width))
        flag = True 
        clock = pygame.time.Clock()
        t = time.clock()
        movimento = None

        while flag:
            pygame.time.delay(50)
            clock.tick(10)

            if movimento != None:
                s.sendall(pickle.dumps(movimento))
                movimento = None
            else:
                s.sendall(pickle.dumps(snakes))  # enviando cobra do cliente pro servidor

            data = s.recv(4096)  # recebendo dados do servidor
            
            if data:
                snakes = pickle.loads(data)  # recebendo outras cobras do servidor
                cobra = snakes.get(client_ip) # cobra do cliente
                # grande gambiarra pra matar quando encostar em alguém
                if cobra:
                    cobras_corpo = []
                    for key in snakes:
                        if type(key) is tuple and snakes[key] != cobra:
                            cobras_corpo.append(positions(snakes[key].body))
                    for x in range(len(cobra.body)):
                        if cobra.body[x].pos in sum(cobras_corpo, []):
                            message_box('Game Over!', 'Score {}'.format(len(cobra.body)))
                            cobra.reset((10,10))
                            exit(1)
            else:
                time.sleep(5)
                continue

            for event in pygame.event.get(): # verificando movimentos
                keys = pygame.key.get_pressed()
                for key in keys:
                    if keys[pygame.K_LEFT]:
                        movimento = 'left'

                    elif keys[pygame.K_RIGHT]:
                        movimento = 'right'

                    elif keys[pygame.K_UP]:
                        movimento = 'up'

                    elif keys[pygame.K_DOWN]:
                        movimento = 'down'

            snacks = snakes.pop('snacks')          
            redrawWindow(win, rows, width, snakes, snacks)
        pass

main()
