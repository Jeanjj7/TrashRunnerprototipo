import pygame
from pygame.locals import *
from sys import exit
from random import randint

# Inicialização
pygame.init()

# Constantes
LARGURA = 1920
ALTURA = 1080
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)
VERMELHO = (200, 0, 0)
AZUL = (50, 50, 255)
CINZA = (150, 150, 150)
CHAO = ALTURA - 150

# Tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Trash Runner")
clock = pygame.time.Clock()

# Carrega imagens
fundo = pygame.image.load("16.png").convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
spritesheet = pygame.image.load("ps1.png").convert_alpha()
img_game_over = pygame.image.load("game_over.png").convert_alpha()
img_game_over = pygame.transform.scale(img_game_over, (800, 300))

# Sons
som_pulo = pygame.mixer.Sound("pulo-luffy.mp3")
som_morte = pygame.mixer.Sound("aiai_1.mp3")
# som_coleta = pygame.mixer.Sound("tom-scream.mp3")

# Estados do jogo
TELA_INICIAL = 0
JOGANDO = 1
GAME_OVER = 2
estado_jogo = TELA_INICIAL
vida = 1
pontuacao = 0
score = 0
velocidade_base = 10
multiplicador_velocidade = 1.0
proxima_meta = 1500
passo_meta = 2000
passo_multiplicador = 0.1

# Movimento do fundo
pos_fundo = 0
velocidade_fundo = 5

# Botões
play_rect = pygame.Rect(LARGURA//2 - 200, 400, 400, 100)
sair_rect = pygame.Rect(LARGURA//2 - 200, 550, 400, 100)
reiniciar_rect = pygame.Rect(LARGURA//2 - 200, 500, 400, 100)

def cortar_spritesheet(sheet, largura, altura):
    sprites = []
    for i in range(sheet.get_width() // largura):
        frame = sheet.subsurface((i * largura, 0, largura, altura))
        sprites.append(frame)
    return sprites

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = cortar_spritesheet(spritesheet, 30, 36)
        self.sprites = [pygame.transform.scale(s, (150, 150)) for s in self.sprites]
        self.frame = 0
        self.image = self.sprites[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.bottom = CHAO
        self.vel_y = 0
        self.pulando = False
        self.contador_animacao = 0

    def update(self):
        self.contador_animacao += 1
        if self.contador_animacao >= 5:
            self.frame = (self.frame + 1) % len(self.sprites)
            self.image = self.sprites[self.frame]
            self.contador_animacao = 0
        self.vel_y += 1
        self.rect.y += self.vel_y
        if self.rect.bottom >= CHAO:
            self.rect.bottom = CHAO
            self.vel_y = 0
            self.pulando = False

    def pular(self):
        if not self.pulando:
            self.vel_y = -30
            self.pulando = True
            som_pulo.play()

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("obstaculo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (180, 180))
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA
        self.rect.y = CHAO - self.rect.height

    def update(self):
        self.rect.x += -velocidade_base * multiplicador_velocidade
        if self.rect.right < 0:
            self.rect.x = LARGURA + randint(300, 600)

class Lixo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lixo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA + randint(600, 1000)
        self.rect.y = CHAO - self.rect.height

    def update(self):
        self.rect.x += -velocidade_base * multiplicador_velocidade
        if self.rect.right < 0:
            self.rect.x = LARGURA + randint(600, 1000)

jogador = Jogador()
obstaculo = Obstaculo()
lixo = Lixo()
todos = pygame.sprite.Group(jogador, obstaculo, lixo)

def desenhar_tela_inicial():
    tela.blit(fundo, (0, 0))
    fonte_titulo = pygame.font.SysFont("Arial Black", 140)
    logo = pygame.image.load("Trash_Runner_logo.png").convert_alpha()
    logo = pygame.transform.scale(logo, (800, 190))
    tela.blit(logo, (LARGURA//2 - logo.get_width()//2, 200))

    fonte_botao = pygame.font.SysFont("Arial", 70, bold=True)
    play = fonte_botao.render("PLAY", True, BRANCO)
    sair = fonte_botao.render("SAIR", True, BRANCO)

    pygame.draw.rect(tela, VERDE, play_rect, border_radius=20)
    pygame.draw.rect(tela, VERMELHO, sair_rect, border_radius=20)
    tela.blit(play, (play_rect.centerx - play.get_width()//2, play_rect.y + 15))
    tela.blit(sair, (sair_rect.centerx - sair.get_width()//2, sair_rect.y + 15))
    pygame.display.flip()

def desenhar_game_over():
    tela.blit(fundo, (0, 0))
    tela.blit(img_game_over, (LARGURA//2 - img_game_over.get_width()//2, 250))

    fonte_botao = pygame.font.SysFont("Arial", 70, bold=True)
    reiniciar = fonte_botao.render(" REINICIAR", True, PRETO)

    pygame.draw.rect(tela, AZUL, reiniciar_rect, border_radius=20)
    tela.blit(reiniciar, (reiniciar_rect.centerx - reiniciar.get_width()//2, reiniciar_rect.y + 15))
    pygame.display.flip()

while True:
    clock.tick(60)

    if estado_jogo == TELA_INICIAL:
        desenhar_tela_inicial()
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            elif evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                if play_rect.collidepoint(evento.pos):
                    estado_jogo = JOGANDO
                    score = 0
                    pontuacao = 0
                    multiplicador_velocidade = 1.0
                    proxima_meta = 1500
                elif sair_rect.collidepoint(evento.pos):
                    pygame.quit()
                    exit()

    elif estado_jogo == JOGANDO:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            elif evento.type == KEYDOWN and evento.key == K_SPACE:
                jogador.pular()

        todos.update()
        score += 1

        if score >= proxima_meta:
            multiplicador_velocidade += passo_multiplicador
            proxima_meta += passo_meta

        if pygame.sprite.collide_rect(jogador, obstaculo):
            vida -= 1
            som_morte.play()
            estado_jogo = GAME_OVER

        if pygame.sprite.collide_rect(jogador, lixo):
            # som_coleta.play()
            pontuacao += 1
            lixo.rect.x = LARGURA + randint(600, 1000)

        # Atualiza posição do fundo
        pos_fundo -= velocidade_fundo
        if pos_fundo <= -LARGURA:
            pos_fundo = 0

        # Desenha fundo em loop
        tela.blit(fundo, (pos_fundo, 0))
        tela.blit(fundo, (pos_fundo + LARGURA, 0))

        todos.draw(tela)

        fonte = pygame.font.SysFont(None, 60)
        tela.blit(fonte.render(f"Distância: {score}", True, BRANCO), (200, 150))
        tela.blit(fonte.render(f"Pontos: {pontuacao}", True, BRANCO), (200, 200))
        tela.blit(fonte.render(f"Velocidade: x{multiplicador_velocidade:.1f}", True, BRANCO), (200, 250))
        pygame.display.flip()

    elif estado_jogo == GAME_OVER:
        desenhar_game_over()
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            elif evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                if reiniciar_rect.collidepoint(evento.pos):
                    vida = 1
                    pontuacao = 0
                    score = 0
                    jogador.rect.y = CHAO - jogador.rect.height
                    jogador.vel_y = 0
                    obstaculo.rect.x = LARGURA
                    lixo.rect.x = LARGURA + randint(600, 1000)
                    multiplicador_velocidade = 1.0
                    proxima_meta = 1500
                    estado_jogo = JOGANDO
