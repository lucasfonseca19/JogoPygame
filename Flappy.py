#**************** Importando Bibliotecas para o Jogo ****************

#region
import os,sys
import pygame, random
from pygame.locals import *
import pygame.freetype
#endregion

# **************** Definindo dimensões da tela do jogo ****************

#region
LARGURA = 400
ALTURA = 800
#endregion

# **************** Definindo Alguns Setups do jogo ****************

#region
LARGURA = 400
VELOCIDADE=10
GRAVIDADE=1
VELOCIDADEJOGO=8
LARGURASOLO= 2*LARGURA
ALTURASOLO=200
LARGURACORONA=80
ALTURACORONA=500
ESPACO=200
FPS=30
SOM={}

fps=pygame.time.Clock()         #Setup do framerate do jogo



#endregion

# **************** Definindo classes dos assets do jogo ****************
## Elas herdam funções da classe sprite do pygame

#region
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
        self.velocidade = - VELOCIDADE-1 

class Solo(pygame.sprite.Sprite):
    def __init__(self,posix):
        #inicializa o construtor sprite do pygame:
        pygame.sprite.Sprite.__init__(self)
        #importando imagem do solo e usando convert alpha para considerar apenas os pixel do icone(sem o fundo)
        self.image = pygame.image.load('base.png').convert_alpha()
        #definindo dimensões do solo
        self.image = pygame.transform.scale(self.image,(LARGURASOLO,ALTURASOLO))

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

class Corona(pygame.sprite.Sprite):
    def __init__(self,inversao,posix,tamanhoy):
         #inicializa o construtor sprite do pygame:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(LARGURACORONA,ALTURACORONA))

        self.rect=self.image.get_rect()
        self.rect[0]=posix
        
        if inversao:
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect[1] = -(self.rect[3]-tamanhoy)
        else:
            self.rect[1]=ALTURA - tamanhoy 
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.rect[0] -= VELOCIDADEJOGO+4
#endregion

# **************** Definindo funções do jogo ****************

## Verificando se algum elemento saiu inteiramente da tela

#region
def foratela(sprite):
    #posicao x do retangulo na tela comparado com sua largura (valor resultante boleano)
    return sprite.rect[0]<-(sprite.rect[2])

## Criação de canos
def randomizacorona(posix):
    
    tamanho = random.randint(200,500)
    corona = Corona(False,posix,tamanho+10)
    corona_invertida = Corona(True,posix,ALTURA-tamanho-ESPACO)
    return (corona,corona_invertida) 

## Verificador de Colisão
def colisao():
    if pygame.sprite.groupcollide(guria_grupo,corona_grupo, False, False, pygame.sprite.collide_mask) or   guria.rect.bottom >= 650:
        return True
    else:
        return False



#endregion

# ****************FUNÇÃO PRINCIPAL DO GAME ****************

pygame.init()
fonte_g=pygame.font.Font("FlappyBirdy.ttf",60)
fonte_p=pygame.font.Font("FlappyBirdy.ttf",40)

## Tela de gameover
def teladegameover():
    pygame.mixer.music.stop()
    tela.blit(FUNDO,(0,0))
    pygame.mixer.music.load('coronamusic.ogg')
    pygame.mixer.music.play()
    sup_tit1=fonte_g.render("Flappy Bird ",False,(221,119,70))
    sup_tit2=fonte_g.render("Coronoa Edition",True,(221,119,70))
    sup_sub1=fonte_p.render("Use a barra para iniciar o jogo ",True,(221,119,70))
    sup_sub2=fonte_p.render("e",True,(221,119,70))
    sup_sub3=fonte_p.render(" para pular",True,(221,119,70))
    tela.blit(sup_tit1,(125,ALTURA/4))
    tela.blit(sup_tit2,(100,ALTURA/3))
    tela.blit(sup_sub1,(50,ALTURA/2))
    tela.blit(sup_sub2,(200,(ALTURA/2)+50))
    tela.blit(sup_sub3,(150,(ALTURA/2)+100))
    pygame.display.flip()
    aguardando=True
    while aguardando:
        fps.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYUP:
                pygame.mixer.music.stop()
                aguardando = False

 


## **************** Settings de Tela ****************
#region
tela=pygame.display.set_mode((LARGURA,ALTURA))   # Criando a tela com as dimensões definidas
pygame.display.set_caption('Flappy Bird - Corona Edition')  # Dando nome pra tela
FUNDO=pygame.image.load("fundo.png")  #Imporatando fundo e definindo uma "variável" para utilizá-lo
gameover=pygame.image.load('gameover.png').convert_alpha()  #importando imagem de game over 
gameover=gameover.get_rect()
FUNDO=pygame.transform.scale(FUNDO,(LARGURA,ALTURA))  #alterando tamanho da imagem do fundo para caber na tela
game_over=True
#endregion





## **************** Grupos de Asset ****************
#region
guria_grupo = pygame.sprite.Group()  #Criando grupo de personagens (facilita manipulação)
guria=Guria()  #Criando obsjeto do tipo Guria
guria_grupo.add(guria)  #Adicionando obejto no grupo

solo_grupo=pygame.sprite.Group()  #Criando grupo de solo (facilita manipulação)
for i in range (2):               #criando um solo em seguida do outro
    solo=Solo(LARGURASOLO*i)
    solo_grupo.add(solo)

corona_grupo = pygame.sprite.Group()  #Criando o grupo do corona (facilita manipulação)
for i in range(2):                      #randomizando corona criando novos e adicionando no grupo
    corona = randomizacorona(400*i+600)
    corona_grupo.add(corona[0])
    corona_grupo.add(corona[1])
#endregion


## **************** LOOP PRINCIPAL DO JOGO ****************
loop=True
while loop:
    if game_over:
        teladegameover()
        game_over = False
        guria_grupo = pygame.sprite.Group()  #Criando grupo de personagens (facilita manipulação)
        guria=Guria()  #Criando obsjeto do tipo Guria
        guria_grupo.add(guria)  #Adicionando obejto no grupo

        solo_grupo=pygame.sprite.Group()  #Criando grupo de solo (facilita manipulação)
        for i in range (2):               #criando um solo em seguida do outro
            solo=Solo(LARGURASOLO*i)
            solo_grupo.add(solo)

        corona_grupo = pygame.sprite.Group()  #Criando o grupo do corona (facilita manipulação)
        for i in range(2):                      #randomizando corona criando novos e adicionando no grupo
            corona = randomizacorona(400*i+600)
            corona_grupo.add(corona[0])
            corona_grupo.add(corona[1])

    fps.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == QUIT:         # Se o usuário apertar no botão (x) de fechar, o jogo é fechado 
            pygame.quit()
        if evento.type == pygame.KEYDOWN:
            if evento.key==K_SPACE:
                guria.pular()        
   
    tela.blit(FUNDO,(0,0))                                   #colocando a imagem de fundo na tela na origem da dela (0,0)
    
    if foratela(solo_grupo.sprites()[0]):                    # teste se o solo está fora da tela
        solo_grupo.remove(solo_grupo.sprites()[0])           #remove o solo na posição 0 do grupo se ele ja saiu da tela
        novosolo=Solo(LARGURASOLO-10)                        #Criando novo solo pra entrar no grupo criando assim um loop de solos consecutivos(o -10 garante um melhor "encaixe" de um no outro)
        solo_grupo.add(novosolo)
    if foratela(corona_grupo.sprites()[0]):                  # teste se o corona está fora da tela 
        corona_grupo.remove(corona_grupo.sprites()[0])
        corona_grupo.remove(corona_grupo.sprites()[0])

        corona = randomizacorona(LARGURA+300)

        corona_grupo.add(corona[0])
        corona_grupo.add(corona[1])

   
    guria_grupo.update()                                    # Update personagem
    guria_grupo.draw(tela)                                  # Colocando o personagem na tela
   

    solo_grupo.update()                                     # Update solo                                         
    solo_grupo.draw(tela)                                   # Colocando solo na tela
    
    corona_grupo.update()                                   # Update obstáculo  
    corona_grupo.draw(tela)                                 # Colocando Obstáculo na tela
    
   
    
    
    
   
    if colisao():                                           # Caso a função colisão retorne True 
        game_over=True
       
        

    #Atualização da tela
    pygame.display.update()
    fps.tick(FPS)


   
 
