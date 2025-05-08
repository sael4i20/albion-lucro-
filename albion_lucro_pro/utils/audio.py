# utils/audio.txt - Sons e Música do App

import pygame
import threading
import os

CAMINHO_CLIQUE = "audio/cliques/click.wav"
CAMINHO_MUSICA = "audio/musica_fundo/music.mp3"

def tocar_som_clique():
    def tocar():
        try:
            pygame.mixer.init()
            if os.path.exists(CAMINHO_CLIQUE):
                click = pygame.mixer.Sound(CAMINHO_CLIQUE)
                click.set_volume(0.5)
                click.play()
        except Exception as e:
            print(f"[Audio] Erro ao tocar clique: {e}")
    threading.Thread(target=tocar).start()

def iniciar_musica_fundo():
    try:
        pygame.mixer.init()
        if os.path.exists(CAMINHO_MUSICA):
            pygame.mixer.music.load(CAMINHO_MUSICA)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"[Audio] Erro ao iniciar música de fundo: {e}")