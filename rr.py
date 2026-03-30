import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

# ===== CONFIG TELA =====
info = pygame.display.Info()
LARGURA = info.current_w
ALTURA = info.current_h

ESCALA_X = LARGURA / 1920
ESCALA_Y = ALTURA / 1080

tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
pygame.display.set_caption("Trash Runner")
clock = pygame.time.Clock()

# ===== CORES =====
BRANCO = (255,255,255)
PRETO = (0,0,0)
VERDE = (0,200,0)
VERMELHO = (200,0,0)
AZUL = (50,50,255)
LARANJA = (255,204,0)

CHAO = ALTURA - int(ALTURA * 0.14)

# ===== ESTADOS =====
TELA_INICIAL = 0
JOGANDO = 1
GAME_OVER = 2
TELA_MISSAO = 3
PAUSADO = 4

estado_jogo = TELA_INICIAL

# ===== BOTÕES =====
play_rect = pygame.Rect(LARGURA//2 - 200, int(400*ESCALA_Y), 400, 100)
sair_rect = pygame.Rect(LARGURA//2 - 200, int(550*ESCALA_Y), 400, 100)
reiniciar_rect = pygame.Rect(LARGURA//2 - 200, int(750*ESCALA_Y), 400, 100)
inicio_rect = pygame.Rect(LARGURA//2 - 200, int(620*ESCALA_Y), 400, 100)
pause_rect = pygame.Rect(LARGURA - 120, 20, 100, 50)

# ===== FUNDO =====
def carregar_fundos(pasta, prefixo):
    fundos = []
    for i in range(1,5):
        img = pygame.image.load(f"{pasta}/{prefixo}{i}.png").convert()
        img = pygame.transform.scale(img, (LARGURA, ALTURA))
        fundos.append(img)
    return fundos

fundos = carregar_fundos("fundo", "f")
fundo_atual = fundos
posicoes_fundos = [i * LARGURA for i in range(len(fundos))]

# ===== IMAGENS =====
spritesheet = pygame.image.load("ps1.png").convert_alpha()
img_lixo = pygame.transform.scale(pygame.image.load("coletadolixo.png").convert_alpha(), (100,100))
img_game_over = pygame.transform.scale(pygame.image.load("game_over.png").convert_alpha(), (800,300))

# ===== SOM =====
pygame.mixer.init()
som_pulo = pygame.mixer.Sound("pulo-luffy.mp3")
som_morte = pygame.mixer.Sound("aiai_1.mp3")
pygame.mixer.music.load("Burn_Rubber.mp3")
pygame.mixer.music.play(-1)

# ===== VARIÁVEIS =====
score = 0
pontuacao = 0
velocidade = 10

# ===== FUNÇÕES =====
def cortar(sheet, w, h):
    return [sheet.subsurface((i*w,0,w,h)) for i in range(sheet.get_width()//w)]

# ===== CLASSES =====
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = [pygame.transform.scale(s,(150,150)) for s in cortar(spritesheet,30,36)]
        self.frame = 0
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.x = int(300*ESCALA_X)
        self.rect.bottom = CHAO
        self.vel = 0
        self.pulando = False

    def update(self):
        self.frame = (self.frame+1)%len(self.sprites)
        self.image = self.sprites[self.frame]

        self.vel += 1
        self.rect.y += self.vel

        if self.rect.bottom >= CHAO:
            self.rect.bottom = CHAO
            self.vel = 0
            self.pulando = False

    def pular(self):
        if not self.pulando:
            self.vel = -30
            self.pulando = True
            som_pulo.play()

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("obstaculo.png").convert_alpha(), (180,180))
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA
        self.rect.y = CHAO - self.rect.height

    def update(self):
        self.rect.x -= velocidade
        if self.rect.right < 0:
            self.rect.x = LARGURA + randint(300,600)

class Lixo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("lixo.png").convert_alpha(), (150,150))
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA + randint(600,1000)
        self.rect.y = CHAO - self.rect.height

    def update(self):
        self.rect.x -= velocidade
        if self.rect.right < 0:
            self.rect.x = LARGURA + randint(600,1000)

# ===== OBJETOS =====
jogador = Jogador()
obstaculo = Obstaculo()
lixo = Lixo()

grupo = pygame.sprite.Group(jogador, obstaculo, lixo)

# ===== LOOP =====
while True:
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()

        if estado_jogo == TELA_INICIAL:
            if evento.type == MOUSEBUTTONDOWN:
                if play_rect.collidepoint(evento.pos):
                    estado_jogo = JOGANDO
                    score = 0
                    pontuacao = 0
                if sair_rect.collidepoint(evento.pos):
                    pygame.quit()
                    exit()

        elif estado_jogo == JOGANDO:
            if evento.type == KEYDOWN and evento.key == K_SPACE:
                jogador.pular()

            if evento.type == MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(evento.pos):
                    estado_jogo = PAUSADO

        elif estado_jogo == PAUSADO:
            if evento.type == MOUSEBUTTONDOWN or evento.type == KEYDOWN:
                estado_jogo = JOGANDO

        elif estado_jogo == GAME_OVER:
            if evento.type == MOUSEBUTTONDOWN:
                if inicio_rect.collidepoint(evento.pos):
                    estado_jogo = TELA_INICIAL
                elif reiniciar_rect.collidepoint(evento.pos):
                    score = 0
                    pontuacao = 0
                    jogador.rect.bottom = CHAO
                    obstaculo.rect.x = LARGURA
                    lixo.rect.x = LARGURA + randint(600,1000)
                    estado_jogo = JOGANDO

    # ===== TELA INICIAL =====
    if estado_jogo == TELA_INICIAL:
        tela.fill(PRETO)

        fonte = pygame.font.SysFont("Arial",70)
        pygame.draw.rect(tela, VERDE, play_rect)
        pygame.draw.rect(tela, VERMELHO, sair_rect)

        tela.blit(fonte.render("PLAY",True,BRANCO),(play_rect.x+120,play_rect.y+20))
        tela.blit(fonte.render("SAIR",True,BRANCO),(sair_rect.x+120,sair_rect.y+20))

    # ===== JOGANDO =====
    elif estado_jogo == JOGANDO:
        tela.fill((30,30,30))

        grupo.update()
        grupo.draw(tela)

        score += 1

        if pygame.sprite.collide_rect(jogador, obstaculo):
            som_morte.play()
            estado_jogo = GAME_OVER

        if pygame.sprite.collide_rect(jogador, lixo):
            pontuacao += 1
            lixo.rect.x = LARGURA + randint(600,1000)

        fonte = pygame.font.SysFont("Arial",40)
        tela.blit(fonte.render(f"Score: {score}",True,BRANCO),(50,50))
        tela.blit(img_lixo,(50,100))
        tela.blit(fonte.render(str(pontuacao),True,BRANCO),(120,110))

        # BOTÃO PAUSA
        pygame.draw.rect(tela, AZUL, pause_rect)
        tela.blit(fonte.render("||",True,BRANCO),(pause_rect.x+30,pause_rect.y+5))

    # ===== PAUSA =====
    elif estado_jogo == PAUSADO:
        tela.fill(PRETO)
        fonte = pygame.font.SysFont("Arial",80)
        tela.blit(fonte.render("PAUSADO",True,BRANCO),(LARGURA//2-150,ALTURA//2))

    # ===== GAME OVER =====
    elif estado_jogo == GAME_OVER:
        tela.fill(PRETO)
        tela.blit(img_game_over,(LARGURA//2-400,150))

        fonte = pygame.font.SysFont("Arial",50)

        pygame.draw.rect(tela, VERDE, inicio_rect)
        pygame.draw.rect(tela, AZUL, reiniciar_rect)

        tela.blit(fonte.render("INICIO",True,BRANCO),(inicio_rect.x+100,inicio_rect.y+20))
        tela.blit(fonte.render("REINICIAR",True,BRANCO),(reiniciar_rect.x+60,reiniciar_rect.y+20))

    pygame.display.flip()