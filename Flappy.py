# Importando bibliotecas

import pygame
from pygame.locals import *

#Definindo dimensões da tela do jogo
LARGURA = 400
ALTURA = 800
#constantes fisicas
VELOCIDADE=2.5
GRAVIDADE=0.08
VELOCIDADEJOGO=10
LARGURASOLO= 2*LARGURA
ALTURASOLO=200
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
#criando classe solo
class Solo(pygame.sprite.Sprite):
    def __init__(self,posix):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(LARGURASOLO,ALTURASOLO))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0]= posix
        self.rect[1]=ALTURA-ALTURASOLO
    def update(self):
        self.rect[0]-=VELOCIDADEJOGO

def foratela(sprite):
    #posicao x do retangulo na tela com sua largura (valor resultante boleano)
    return sprite.rect[0]<-(sprite.rect[2])


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
#criando grupo de solo
solo_grupo=pygame.sprite.Group()
for i in range (2):
    solo=Solo(LARGURASOLO*i)
    solo_grupo.add(solo)

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
    # teste se solo fora da tela    
    if foratela(solo_grupo.sprites()[0]):
        solo_grupo.remove(solo_grupo.sprites()[0])
        novosolo=Solo(LARGURASOLO-20)
        solo_grupo.add(novosolo)
    #modificações do personagem
    guria_grupo.update()
    #alteraçao solo
    solo_grupo.update()
    #colocando o personagem na tela
    guria_grupo.draw(tela)
    #colocando solo na tela
    solo_grupo.draw(tela)
    
    
    pygame.display.update()
    
