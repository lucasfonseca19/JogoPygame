# Importando bibliotecas
 
import pygame
from pygame.locals import *

#Definindo dimensões da tela do jogo
LARGURA = 400
ALTURA = 800
#Constantes fisicas
VELOCIDADE=10
GRAVIDADE=1
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
        # criando mascara de valores 0 e 1 (0 para pixel vazio e 1 para pixel com alguma cor) Isso sera usado para checar a colisão que ocorrerá apenas quando um pixel 1 de um grupo encontar em outro grupo um pixel igual(1)
        self.mask = pygame.mask.from_surface(self.image)
        #Determinando a velocidade inicial do objeto
        self.velocidade = VELOCIDADE
        #posição e tamanho do personagem. Rect é considerado uma tulpa com 4 informações : [0]=Posição x na tela [1]= Posição y na tela [2] = Comprimento do objeto [3]= Altura do objeto
        self.rect = self.image.get_rect()
        self.rect.center=(LARGURA/2,ALTURA/2)
    #atualização do sprite com o tempo   
    def update(self):
        #impõe uma taxa de variação para a velocidade
        self.velocidade += GRAVIDADE
        #update da altura
        self.rect[1] += self.velocidade
    #sprite pula
    def pular(self):
        self.velocidade =- VELOCIDADE
#criando classe solo(ela herda funções da classe sprite do pygame)
class Solo(pygame.sprite.Sprite):
    def __init__(self,posix):
        #inicializa o construtor sprite do pygame:
        pygame.sprite.Sprite.__init__(self)
        #importando imagem do solo e usando convert alpha para considerar apenas os pixel do icone(sem o fundo)
        self.image = pygame.image.load('base.png').convert_alpha()
        #definindo dimensões do solo
        self.image = pygame.transform.scale(self.image,(LARGURASOLO,ALTURASOLO))
        #criando mascara de valores 0 e 1 (0 para pixel vazio e 1 para pixel com alguma cor) Isso sera usado para checar a colisão que ocorrerá apenas quando um pixel 1 de um grupo encontar em outro grupo um pixel igual(1)
        self.mask = pygame.mask.from_surface(self.image)
        # transformando imagem num "retângulo" para facilitar seu uso com pygame
        self.rect = self.image.get_rect()
        #Posicionando o solo de acordo com a posição x ('posix') passada como argumento da classe
        self.rect[0]= posix
        #Posicionando o solo na posição vertical correta
        self.rect[1]=ALTURA-ALTURASOLO
    #atualização do sprite com o tempo
    def update(self):
        #update da posição x
        self.rect[0]-=VELOCIDADEJOGO
#função para verificar se algum elemento saiu inteiramente da tela
def foratela(sprite):
    #posicao x do retangulo na tela comparado com sua largura (valor resultante boleano)
    return sprite.rect[0]<-(sprite.rect[2])
def colide(sprite1,sprite2):
    return sprite1.rect[1]==sprite2.rect[3]


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

#criando um solo em seguida do outro
for i in range (2):
    solo=Solo(LARGURASOLO*i)
    solo_grupo.add(solo)
#Setup do framerate do jogo
fps=pygame.time.Clock()
#LOOP PRINCIPAL DO JOGO
while True:
    fps.tick(24)
    for evento in pygame.event.get():
        # Se o usuário apertar no botão (x) de fechar, o jogo é fechado 
        if evento.type == QUIT:
            pygame.quit()
        if evento.type == pygame.KEYDOWN:
            if evento.key==K_SPACE:
                guria.pular()        
    #colocando a imagem de fundo na tela na origem da dela (0,0)
    tela.blit(FUNDO,(0,0))
    # teste se o solo está fora da tela    
    if foratela(solo_grupo.sprites()[0]):
        #remove o solo na posição 0 do grupo se ele ja saiu da tela
        solo_grupo.remove(solo_grupo.sprites()[0])
        #criando novo solo pra entrar no grupo criando assim um loop de solos consecutivos(o -10 garante um melhor "encaixe" de um no outro)
        novosolo=Solo(LARGURASOLO-10)
        solo_grupo.add(novosolo)
    #modificações do personagem
    guria_grupo.update()
    #alteraçao solo
    solo_grupo.update()
    #colocando o personagem na tela
    guria_grupo.draw(tela)
    #colocando solo na tela
    solo_grupo.draw(tela)
    

    
    #Atualização da tela
    pygame.display.update()
    #Checar colisão entre personagem em solo
    if colide(guria_grupo.sprites()[0],solo_grupo.sprites()[1]):
        input()
        break 
