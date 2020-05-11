# Importando bibliotecas

import pygame
from pygame.locals import *

#Definindo dimensões da tela do jogo

LARGURA = 500
ALTURA = 800

#função que inicializa o pygame
pygame.init()
# Criando a tela com as dimensões definidas
tela=pygame.display.set_mode((LARGURA,ALTURA))
#imporatando fundo e definindo uma "variável" para utilizá-lo
FUNDO=pygame.image.load("fundo.png")
#alterando tamanho da imagem do fundo para caber na tela
FUNDO=pygame.transform.scale(FUNDO,(LARGURA,ALTURA))

#loop principal do game 
while True:
    for evento in pygame.event.get():
        # Se o usuário apertar no botão (x) de fechar, o jogo é fechado 
        if evento.type == QUIT:
            pygame.quit()
    tela.blit(FUNDO,(0,0))
    
    
    
    
    
    
    pygame.display.update()
    
