import pygame
from pygame.locals import *
from sys import exit
from random import randint

# Inicialização
pygame.init()

# Constantes
LARGURA = 1280
ALTURA = 720
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)
VERMELHO = (200, 0, 0)
AZUL = (50, 50, 255)
CINZA = (150, 150, 150)
CHAO = ALTURA - 100

# Tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Trash Runner")
clock = pygame.time.Clock()

# Carrega imagem de fundo
fundo = pygame.image.load("bar1.png").convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

# Estados do jogo
TELA_INICIAL = 0
JOGANDO = 1
GAME_OVER = 2

estado_jogo = TELA_INICIAL
vida = 1
pontuacao = 0
score = 0

# Dificuldade progressiva
velocidade_base = 10
multiplicador_velocidade = 1.0
proxima_meta = 1500
passo_meta = 2000
passo_multiplicador = 0.1

# Carrega spritesheet
spritesheet = pygame.image.load("ps1.png").convert_alpha()

# Função para cortar os quadros da spritesheet
def cortar_spritesheet(sheet, largura, altura):
    sprites = []
    for i in range(sheet.get_width() // largura):
        frame = sheet.subsurface((i * largura, 0, largura, altura))
        sprites.append(frame)
    return sprites

# Personagem com animação
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = cortar_spritesheet(spritesheet, 30, 36)
        self.sprites = [pygame.transform.scale(s, (100, 100)) for s in self.sprites]
        self.frame = 0
        self.image = self.sprites[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = CHAO - 100
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
        if self.rect.y >= CHAO - self.rect.height:
            self.rect.y = CHAO - self.rect.height
            self.vel_y = 0
            self.pulando = False

    def pular(self):
        if not self.pulando:
            self.vel_y = -25
            self.pulando = True

# Obstáculo
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA
        self.rect.y = CHAO - 100

    def update(self):
        self.rect.x += -velocidade_base * multiplicador_velocidade
        if self.rect.right < 0:
            self.rect.x = LARGURA + randint(200, 500)

# Lixo com imagem pixel art
class Lixo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lixo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))  # Ajuste conforme desejar
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA + randint(500, 1000)
        self.rect.y = CHAO - self.rect.height

    def update(self):
        self.rect.x += -velocidade_base * multiplicador_velocidade
        if self.rect.right < 0:
            self.rect.x = LARGURA + randint(500, 1000)

# Instâncias
jogador = Jogador()
obstaculo = Obstaculo()
lixo = Lixo()
todos = pygame.sprite.Group()
todos.add(jogador, obstaculo, lixo)

# Telas
def desenhar_tela_inicial():
    tela.blit(fundo, (0, 0))
    fonte = pygame.font.SysFont(None, 80)
    titulo = fonte.render("Trash Runner", True, BRANCO)
    jogar = fonte.render("Pressione [J] para Jogar", True, VERDE)
    sair = fonte.render("Pressione [S] para Sair", True, VERMELHO)
    tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 200))
    tela.blit(jogar, (LARGURA//2 - jogar.get_width()//2, 350))
    tela.blit(sair, (LARGURA//2 - sair.get_width()//2, 450))
    pygame.display.flip()

def desenhar_game_over():
    tela.blit(fundo, (0, 0))
    fonte = pygame.font.SysFont(None, 80)
    texto = fonte.render("Game Over!", True, BRANCO)
    reiniciar = fonte.render("Pressione [R] para Reiniciar", True, AZUL)
    tela.blit(texto, (LARGURA//2 - texto.get_width()//2, 300))
    tela.blit(reiniciar, (LARGURA//2 - reiniciar.get_width()//2, 400))
    pygame.display.flip()

# Loop principal
while True:
    clock.tick(60)

    if estado_jogo == TELA_INICIAL:
        desenhar_tela_inicial()
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            if evento.type == KEYDOWN:
                if evento.key == K_j:
                    estado_jogo = JOGANDO
                    score = 0
                    pontuacao = 0
                    multiplicador_velocidade = 1.0
                    proxima_meta = 1500
                elif evento.key == K_s:
                    pygame.quit()
                    exit()

    elif estado_jogo == JOGANDO:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            if evento.type == KEYDOWN and evento.key == K_SPACE:
                jogador.pular()

        todos.update()
        score += 1

        if score >= proxima_meta:
            multiplicador_velocidade += passo_multiplicador
            proxima_meta += passo_meta

        if pygame.sprite.collide_rect(jogador, obstaculo):
            vida -= 1
            estado_jogo = GAME_OVER

        if pygame.sprite.collide_rect(jogador, lixo):
            pontuacao += 1
            lixo.rect.x = LARGURA + randint(500, 1000)

        tela.blit(fundo, (0, 0))
        todos.draw(tela)

        fonte = pygame.font.SysFont(None, 50)
        tela.blit(fonte.render(f"Distância: {score}", True, BRANCO), (30, 30))
        tela.blit(fonte.render(f"Pontos: {pontuacao}", True, BRANCO), (30, 70))
        tela.blit(fonte.render(f"Velocidade: x{multiplicador_velocidade:.1f}", True, BRANCO), (30, 110))

        pygame.display.flip()

    elif estado_jogo == GAME_OVER:
        desenhar_game_over()
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            if evento.type == KEYDOWN and evento.key == K_r:
                vida = 1
                pontuacao = 0
                score = 0
                jogador.rect.y = CHAO - jogador.rect.height
                jogador.vel_y = 0
                obstaculo.rect.x = LARGURA
                lixo.rect.x = LARGURA + randint(500, 1000)
                multiplicador_velocidade = 1.0
                proxima_meta = 1500
                estado_jogo = JOGANDO
