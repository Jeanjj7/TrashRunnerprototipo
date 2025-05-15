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
pontuacao = 0
score = 0

# Variáveis de dificuldade progressiva
velocidade_base = 10
multiplicador_velocidade = 1.0
proxima_meta = 1500
passo_meta = 2000
passo_multiplicador = 0.1

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

    def update(self):
        self.rect.x += -velocidade_base * multiplicador_velocidade
        if self.rect.right < 0:
            self.rect.x = LARGURA + randint(200, 500)

# Lixo
class Lixo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(CINZA)
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA + randint(500, 1000)
        self.rect.y = CHAO - 40

    def update(self):
        self.rect.x += -velocidade_base * multiplicador_velocidade
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

# Telas
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
                    score = 0
                    multiplicador_velocidade = 1.0
                    proxima_meta = 1500
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

        # Atualização de sprites
        todos.update()
        score += 1

        # Verifica meta de distância para aumento de velocidade
        if score >= proxima_meta:
            multiplicador_velocidade += passo_multiplicador
            proxima_meta += passo_meta

        # Colisões
        if pygame.sprite.collide_rect(jogador, obstaculo):
            vida -= 1
            estado_jogo = GAME_OVER

        if pygame.sprite.collide_rect(jogador, lixo):
            pontuacao += 1
            lixo.rect.x = LARGURA + randint(500, 1000)

        # Desenho
        tela.fill(BRANCO)
        pygame.draw.line(tela, PRETO, (0, CHAO), (LARGURA, CHAO), 5)
        todos.draw(tela)

        fonte_score = pygame.font.SysFont(None, 50)
        texto_tempo = fonte_score.render(f"Distancia : {score}", True, PRETO)
        texto_pontos = fonte_score.render(f"Pontos: {pontuacao}", True, PRETO)
        texto_velocidade = fonte_score.render(f"Velocidade: x{multiplicador_velocidade:.1f}", True, PRETO)
        tela.blit(texto_tempo, (30, 30))
        tela.blit(texto_pontos, (30, 70))
        tela.blit(texto_velocidade, (30, 110))

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
                    multiplicador_velocidade = 1.0
                    proxima_meta = 1500
                    estado_jogo = JOGANDO
