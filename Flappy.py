# Importando bibliotecas

import pygame
from pygame.locals import *

#Definindo dimensões da tela do jogo
LARGURA = 400
ALTURA = 800
#constantes fisicas
VELOCIDADE=2.5
GRAVIDADE=0.08
#criando classe do personagem (ela herda funções da classe sprite do pygame)
class Guria(pygame.sprite.Sprite):
    def __init__(self):
        #inicializa o construtor sprite do pygame:
        pygame.sprite.Sprite.__init__(self)  
        #importando imagem do personagem e usando convert alpha para considerar apenas os pixel do icone(sem o fundo)
        self.image = pygame.image.load('guria.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(100,100))
        self.velocidade = VELOCIDADE
        #posição e tamanho do personagem
        self.rect = self.image.get_rect()
        self.rect.center=(LARGURA/2,ALTURA/2)
    #atualização do sprite com o tempo   
    def update(self):
        self.velocidade += GRAVIDADE
        #update da altura
        self.rect[1] += self.velocidade
    #sprite pula
    def pular(self):
        self.velocidade =- VELOCIDADE
#função que inicializa o pygame
pygame.init()
# Criando a tela com as dimensões definidas
tela=pygame.display.set_mode((LARGURA,ALTURA))
#imporatando fundo e definindo uma "variável" para utilizá-lo
FUNDO=pygame.image.load("fundo.png")
#alterando tamanho da imagem do fundo para caber na tela
FUNDO=pygame.transform.scale(FUNDO,(LARGURA,ALTURA))
#Criando grupo de personagens
guria_grupo = pygame.sprite.Group()
#criando obsjeto do tipo Guria
guria=Guria()
#adicionando obejto no grupo
guria_grupo.add(guria)
#loop principal do game 
while True:
   
    for evento in pygame.event.get():
        # Se o usuário apertar no botão (x) de fechar, o jogo é fechado 
        if evento.type == QUIT:
            pygame.quit()
        if evento.type == pygame.KEYDOWN:
            if evento.key==K_SPACE:
                guria.pular()
    #colocando a imagem de fundo na tela na origem da dela (0,0)
    tela.blit(FUNDO,(0,0))            
    #modificações do personagem
    guria_grupo.update()
    #colocando o personagem na tela
    guria_grupo.draw(tela)
    
    
    
    pygame.display.update()
    
