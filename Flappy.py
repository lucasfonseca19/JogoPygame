#**************** Importando Bibliotecas para o Jogo ****************

#region
import pygame, random
from pygame.locals import *
#endregion

# **************** Definindo dimensões da tela do jogo ****************

#region
LARGURA = 600
ALTURA = 700
#endregion

# **************** Definindo Alguns Setups do jogo ****************

#region
pygame.init() # "Inicializa todos os módulos de pygame importados"
VELOCIDADE=12 
GRAVIDADE=1.5
VELOCIDADEJOGO=12
LARGURASOLO= 2*LARGURA
ALTURASOLO=100
LARGURACANO=80
ALTURACANO=500
ESPACO=200                              # Espaço entre cano superior e inferior
FPS=30                                  # Frames por segundo 
SOM={}                                  # Dicionario de som
pygame.mixer.init()                     # Iniciando o modulo de mixagem de som do pygame
SOM["tela_inicial"]=pygame.mixer.Sound('coronamusic.ogg') 
SOM["pular"]=pygame.mixer.Sound('pulo.ogg')
SOM["colisao"]=pygame.mixer.Sound('colisao.ogg')
SOM["ponto"]=pygame.mixer.Sound('ponto.ogg')
fps=pygame.time.Clock()                # Setup do framerate do jogo (valor atribuido posteriormente)
pontos=0                               # Pontos obtidos quando o personagem passa por uma dupla de canos(superior e inferior)
numero=0                               # "Código de série" de cada dupla de canos. Esse valor é iterado e cada dupla de canos possui o valor da anterior + 1
fonte_g=pygame.font.Font("FlappyBirdy.ttf",80)  # Criando fonte grande para o título
fonte_p=pygame.font.Font("FlappyBirdy.ttf",60)  # Criando fonte pequena para as instruções de jogo
fonte_pts = pygame.font.Font("fonte.ttf",30)  # Criando fonte para pontuação durante o jogo e pontuação final

#endregion

# **************** Definindo classes dos assets do jogo ****************
## Elas herdam funções da classe sprite do pygame

#region
class Guria(pygame.sprite.Sprite):
    """ Esta classe refere-se à personagem do jogo """
    def __init__(self):
        """ Iniciando construtor de classes """
        pygame.sprite.Sprite.__init__(self)  #Inicializa o construtor sprite do pygame:
        self.image = pygame.image.load('guria.png').convert_alpha() #Importando imagem do personagem e usando convert alpha para considerar apenas os pixel do icone(sem o fundo)
        self.image = pygame.transform.scale(self.image,(100,100))  #Alterando o tamanho da imagem
        self.mask = pygame.mask.from_surface(self.image)  # criando mascara de valores 0 e 1 (0 para pixel vazio e 1 para pixel com alguma cor) Isso sera usado para checar a colisão que ocorrerá apenas quando um pixel 1 de um grupo encontar em outro grupo um pixel igual(1)
        self.velocidade = VELOCIDADE   #Determinando a velocidade inicial do objeto
        self.rect = self.image.get_rect()   #Criando um retângulo com a imagem(útil para utilização de funções do pygame).Rect é considerado uma tulpla com 4 informações : [0]=Posição x na tela [1]= Posição y na tela [2] = Comprimento do objeto [3]= Altura do objeto
        self.rect.center=(LARGURA/2,ALTURA/2)   #Posição inicial da personagem. 
    
    def update(self): 
        """Atualização do sprite da personagem """   
        self.velocidade += GRAVIDADE  #Impõe uma taxa de variação para a velocidade 
        self.rect[1] += self.velocidade  #Update da altura
    
    def pular(self):
        """ função de 'pulo' da personagem """
        self.velocidade = - VELOCIDADE-1 
        
class Solo(pygame.sprite.Sprite):
    """ Esta classe refere-se ao solo do jogo """
    def __init__(self,posix):
        """ Iniciando construtor de classes """
        pygame.sprite.Sprite.__init__(self)  #Inicializa o construtor sprite do pygame
        self.image = pygame.image.load('base.png').convert_alpha()  #Importando imagem do solo e usando convert alpha para considerar apenas os pixel do icone(sem o fundo)
        self.image = pygame.transform.scale(self.image,(LARGURASOLO,ALTURASOLO))  #Definindo dimensões do solo
        self.mask = pygame.mask.from_surface(self.image)  # criando mascara de valores 0 e 1 (0 para pixel vazio e 1 para pixel com alguma cor) Isso sera usado para checar a colisão que ocorrerá apenas quando um pixel 1 de um grupo encontar em outro grupo um pixel igual(1)
        self.rect = self.image.get_rect()  # transformando imagem num "retângulo" para facilitar seu uso com pygame
        self.rect[0]= posix  #Posicionando o solo de acordo com a posição x ('posix') passada como argumento da classe
        self.rect[1]=ALTURA-ALTURASOLO   #Posicionando o solo na posição vertical correta
    
    def update(self):
        """Atualização do sprite do solo"""  
        self.rect[0]-=VELOCIDADEJOGO  #Update da posição x

class Cano(pygame.sprite.Sprite):
    """ Esta classe refere-se ao obstáculo do jogo """
    def __init__(self,inversao,posix,tamanhoy,numero):
        """ Iniciando construtor de classes """
        pygame.sprite.Sprite.__init__(self)  #Inicializa o construtor sprite do pygame
        self.image = pygame.image.load('pipe-red.png').convert_alpha()   #Importando imagem do solo e usando convert alpha para considerar apenas os pixel do icone(sem o fundo)
        self.image = pygame.transform.scale(self.image,(LARGURACANO,ALTURACANO))  #Definindo dimensões do cano
        self.rect=self.image.get_rect()  # transformando imagem num "retângulo" para facilitar seu uso com pygame
        self.rect[0]=posix  #Posicionando o cano de acordo com a posição x ('posix') passada como argumento da classe
        self.numero=numero-2  #Atribuindo um "Número de série" para o objeto de classe Cano (Usado no sistema de pontuação)
        if inversao:  #Quando o argumento inversão é verdadeiro, o cano é reposicionado para criar o cano superior da dupla de canos
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect[1] = -(self.rect[3]-tamanhoy)
        else:
            self.rect[1]=ALTURA - tamanhoy 
        self.mask = pygame.mask.from_surface(self.image)   # criando mascara de valores 0 e 1 (0 para pixel vazio e 1 para pixel com alguma cor) Isso sera usado para checar a colisão que ocorrerá apenas quando um pixel 1 de um grupo encontar em outro grupo um pixel igual(1)
    def update(self):
        """Atualização do sprite cano"""
        self.rect[0] -= VELOCIDADEJOGO+4 #Alterando posição x do cano
#endregion

# **************** Definindo funções do jogo ****************

#region
def foratela(sprite):
    """Verifica se algum elemento saiu inteiramente da tela do jogo"""          
    return sprite.rect[0]<-(sprite.rect[2])   #posicao x do retangulo na tela comparado com sua largura (valor resultante boleano)

def randomizacano(posix):
    global numero
    """Cria dupla de canos randomicamente (Com algumas limitações para correto funcionamento do jogo) """
    numero+=1  #Iterando o valor de número para a atribuição de números de série em sequência 
    tamanho = random.randint(150 ,450)  #Altera o tamanho do cano dentro do range especificado
    cano = Cano(False,posix,tamanho,numero)  #Cria o cano inferior da dupla de canos
    cano_invertido = Cano(True,posix,ALTURA-tamanho-ESPACO,numero)  #Cria o cano superior da dupla de canos
    return (cano,cano_invertido)   

def colisao():
    """Verificador de Colisão"""
    if pygame.sprite.groupcollide(guria_grupo,cano_grupo, False, False, pygame.sprite.collide_mask) or   guria.rect.bottom >= 610:
        return True
    else:
        return False

def pontua(sprite1,sprite2):
    global pontos
    """Altera pontuação ao passar pelos canos sem nenhuma colisão """
    meio_cano=sprite2.rect[0]+sprite2.rect[2]/2  #Ponto médio do cano
    meia_guria=sprite1.rect[0]+sprite1.rect[2]/2 #Ponto médio da personagem
    if meio_cano<=meia_guria:  #Condição para pontuação 
        if sprite2.numero > pontos:  #Atribui o numero de série como o novo valor de pontos se, e somente, se esse numero de série dor maior do que o número atual de pontos
            SOM['ponto'].play()  #Ativa som ao pontuar
            pontos=sprite2.numero  #A pontuação pega o número de série do cano. Como esse número de série é sequencial (Canos 1, Canos 2 ...) essa foi a alternativa adotada para a pontuação.
            
def ponto_tela(superficie,texto,x,y):
    """ Função para mostrar os pontos na tela (criada após o pygame.init por utilizar de seus módulos)"""
    sup_pts  = fonte_pts.render((texto),True,(250,250,250))  #Cria superfície renderizada a partir de um texto. Argumento:texto,Anti-Aliasing e cor.
    pts_rect = sup_pts.get_rect()  #Criando retângulo da superfície
    pts_rect.midtop = (x,y)  #Posicionando o texto na tela
    superficie.blit(sup_pts,pts_rect)  #Colocando o texto na tela

def teladegameover():
    """ Tela tanto de início, como de gameover do jogo. """
    tela.blit(FUNDO,(0,0))  # Mostra somente a imagem de fundo de nosso jogo. "Limpa" qualquer outro asset na tela.
    pygame.time.delay(1000) # Pequeno delay de 1s para iniciar tanto o som, quanto as imagens restantes.
    SOM["tela_inicial"].play(0,0,500) #Música tema (Fade-in de 0.5s)
    # Renderizando texto para plotá-los na tela
    sup_tit1=fonte_g.render("Flappy Bird ",False,(221,119,70))
    sup_tit2=fonte_g.render("Corona Edition",True,(221,119,70))
    sup_sub1=fonte_p.render("Use a barra para iniciar o jogo ",True,(221,119,70))
    sup_sub2=fonte_p.render("e",True,(221,119,70))
    sup_sub3=fonte_p.render(" para pular",True,(221,119,70))
    # Colocando textos na tela
    tela.blit(sup_tit1,(200,ALTURA/4))
    tela.blit(sup_tit2,(150,ALTURA/3))
    tela.blit(sup_sub1,(75,ALTURA/2))
    tela.blit(sup_sub2,(300,(ALTURA/2)+50))
    tela.blit(sup_sub3,(215,(ALTURA/2)+100))
    
    if pontos != 0:  # Caso se tenha feito ao menos um ponto. (Condição esperada após o usuário jogar) é plotado nessa tela a pontuação atingida pelo usuário na partida.
        ponto_tela(tela,("Total: {0} ponto(s) :)".format(str(pontos))),300,10)
    pygame.display.flip()  # Garante o update da tela toda
    aguardando=True  #Usado para permanecer nessa tela até algo acontecer
    while aguardando:  #Permanece na tela até o usuário pressionar e soltar a barra de espaço
        fps.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:     # Se apertar o X para sair do jogo a tela é fechada
                pygame.quit()
                
            if event.type == pygame.KEYUP:
                if event.key==K_SPACE:       # Ao soltar a tecla de espaço, sai da tela de game over/ inicio e o som diminui até parar (fadeout)
                    SOM["tela_inicial"].fadeout(500)
                    aguardando = False
#endregion 

## **************** Settings de Tela ****************

#region
tela=pygame.display.set_mode((LARGURA,ALTURA))   # Criando a tela com as dimensões definidas
pygame.display.set_caption('Flappy Bird - Corona Edition')  # Dando nome pra tela
FUNDO=pygame.image.load("fundo.png")  #Imporatando fundo e definindo uma "variável" para utilizá-lo
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

cano_grupo = pygame.sprite.Group()  #Criando o grupo do Cano (facilita manipulação)
for i in range(2):                      #randomizando Canos, criando novos, e adicionando em um grupo
    cano = randomizacano(400*i+600)     # Valor inicial de 600 pixels para o jogador conseguir avistar os canos
    cano_grupo.add(cano[0])
    cano_grupo.add(cano[1])
#endregion

## **************** LOOP PRINCIPAL DO JOGO ****************

#region
loop=True
while loop:
    if game_over:  # Mostra tela inicial/ gameover e reinicia os parâmetro necessários
        numero = 2 # Parâmetro determinado para melhor funcionamento da função pontua
        teladegameover() 
        pontos = 0 # Pontuação zerada
        game_over = False
        guria_grupo = pygame.sprite.Group()  # Criando grupo de personagens (facilita manipulação)
        guria=Guria()  # Criando objeto do tipo Guria
        guria_grupo.add(guria)  # Adicionando objeto no grupo


        solo_grupo=pygame.sprite.Group()  # Criando grupo de solo (facilita manipulação)
        for i in range (2):               # Criando um solo em seguida do outro
            solo=Solo(LARGURASOLO*i)
            solo_grupo.add(solo)

        cano_grupo = pygame.sprite.Group()  # Criando o grupo do Cano (facilita manipulação)
        for i in range(2):                      # Randomizando Cano criando novos e adicionando no grupo
            cano = randomizacano(400*i+600)
            cano_grupo.add(cano[0])
            cano_grupo.add(cano[1])

    fps.tick(FPS)  # Determina o fps do jogo (frames por segundo)
    for evento in pygame.event.get():
        if evento.type == QUIT:         # Se o usuário apertar no botão (x) de fechar, o jogo é fechado 
            pygame.quit()
        if evento.type == pygame.KEYDOWN: 
            if evento.key==K_SPACE:  # Captura se a barra foi pressioanada para ativar a função pular da classe da personagem.
                SOM["pular"].play() 
                guria.pular()
 
    tela.blit(FUNDO,(0,0))                                   # Colocando a imagem de fundo na tela na origem da dela (0,0)
    
    if foratela(solo_grupo.sprites()[0]):                    # Teste se o solo está fora da tela
        solo_grupo.remove(solo_grupo.sprites()[0])           # Remove o solo na posição 0 do grupo se ele ja saiu da tela
        novosolo=Solo(LARGURASOLO-10)                        # Criando novo solo pra entrar no grupo criando assim um loop de solos consecutivos(o -10 garante um melhor "encaixe" de um no outro)
        solo_grupo.add(novosolo)
    if foratela(cano_grupo.sprites()[0]):                    # Teste se o Cano está fora da tela 
        cano_grupo.remove(cano_grupo.sprites()[0])           # Removendo cano inferior
        cano_grupo.remove(cano_grupo.sprites()[0])           # Removendo cano superior que passa a ser elemento de indice 0 após remoção do inferior

        cano = randomizacano(LARGURA+175)                    # Criando nova dupla de canos 

        cano_grupo.add(cano[0])                              # Adicionando novo cano inferior no grupo
        cano_grupo.add(cano[1])                              # Adicionando novo cano superior no grupo

    guria_grupo.update()                                    # Update personagem
    guria_grupo.draw(tela)                                  # Colocando o personagem na tela
   
    solo_grupo.update()                                     # Update solo                                         
    solo_grupo.draw(tela)                                   # Colocando solo na tela
    
    cano_grupo.update()                                   # Update obstáculo  
    cano_grupo.draw(tela)                                 # Colocando Obstáculo na tela
    
    ponto_tela(tela,str(pontos),300,10)                   # Plotando pontuação na tela durante o jogo
    
    pontua(guria_grupo.sprites()[0],cano_grupo.sprites()[0])  # Verificando se ocorreu pontuação e alterando os pontos se positivo
    
    if colisao():                                           # Caso a função colisão retorne True 
        SOM["colisao"].play()
        game_over=True                                     # game_over passa a ser true: reseta parâmetros necessários e mostra tela de gameover

    #Atualização da tela
    pygame.display.update()
    fps.tick(FPS)
#endregion


   
 
