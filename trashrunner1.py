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
CHAO = ALTURA - 100

# Tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Trash Runner")
clock = pygame.time.Clock()

# Estados do jogo
TELA_INICIAL = 0
JOGANDO = 1
GAME_OVER = 2

estado_jogo = TELA_INICIAL
vida = 1
pontuacao = 0  # coleta de lixo
score = 0      # tempo de sobrevivência

# Personagem
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = CHAO - 80
        self.vel_y = 0
        self.pulando = False

    def update(self):
        self.vel_y += 1
        self.rect.y += self.vel_y

        if self.rect.y >= CHAO - 80:
            self.rect.y = CHAO - 80
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
        self.image = pygame.Surface((60, 100))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA
        self.rect.y = CHAO - 100
        self.vel_x = -10

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.right < 0:
            self.rect.x = LARGURA + randint(200, 500)

# Lixo (coletável)
class Lixo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(CINZA)
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA + randint(500, 1000)
        self.rect.y = CHAO - 40
        self.vel_x = -10

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.right < 0:
            self.rect.x = LARGURA + randint(500, 1000)

# Instâncias
jogador = Jogador()
obstaculo = Obstaculo()
lixo = Lixo()
todos = pygame.sprite.Group()
todos.add(jogador)
todos.add(obstaculo)
todos.add(lixo)

# Tela inicial
def desenhar_tela_inicial():
    tela.fill(BRANCO)
    fonte = pygame.font.SysFont(None, 80)
    titulo = fonte.render("Trash Runner", True, PRETO)
    jogar = fonte.render("Pressione [J] para Jogar", True, VERDE)
    sair = fonte.render("Pressione [S] para Sair", True, VERMELHO)
    tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 200))
    tela.blit(jogar, (LARGURA//2 - jogar.get_width()//2, 350))
    tela.blit(sair, (LARGURA//2 - sair.get_width()//2, 450))
    pygame.display.flip()

# Tela de Game Over
def desenhar_game_over():
    tela.fill(BRANCO)
    fonte = pygame.font.SysFont(None, 80)
    texto = fonte.render("Game Over!", True, PRETO)
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
                if evento.key == K_s:
                    pygame.quit()
                    exit()

    elif estado_jogo == JOGANDO:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            if evento.type == KEYDOWN:
                if evento.key == K_SPACE:
                    jogador.pular()

        todos.update()
        score += 1  # aumenta o score com o tempo (a cada frame)

        # Colisão com obstáculo
        if pygame.sprite.collide_rect(jogador, obstaculo):
            vida -= 1
            estado_jogo = GAME_OVER

        # Coleta de lixo
        if pygame.sprite.collide_rect(jogador, lixo):
            pontuacao += 1
            lixo.rect.x = LARGURA + randint(500, 1000)

        tela.fill(BRANCO)
        pygame.draw.line(tela, PRETO, (0, CHAO), (LARGURA, CHAO), 5)
        todos.draw(tela)

        # Mostrar score e pontuação
        fonte_score = pygame.font.SysFont(None, 50)
        texto_tempo = fonte_score.render(f"Distancia : {score}", True, PRETO)
        texto_pontos = fonte_score.render(f"Pontos: {pontuacao}", True, PRETO)
        tela.blit(texto_tempo, (30, 30))
        tela.blit(texto_pontos, (30, 70))

        pygame.display.flip()

    elif estado_jogo == GAME_OVER:
        desenhar_game_over()
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            if evento.type == KEYDOWN:
                if evento.key == K_r:
                    vida = 1
                    pontuacao = 0
                    score = 0
                    jogador.rect.y = CHAO - 80
                    jogador.vel_y = 0
                    obstaculo.rect.x = LARGURA
                    lixo.rect.x = LARGURA + randint(500, 1000)
                    estado_jogo = JOGANDO
