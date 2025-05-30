import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

# Constantes
LARGURA = 1920
ALTURA = 1080
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)
VERDE_ESCURO = (0, 100, 0)
VERMELHO = (200, 0, 0)
AZUL = (50, 50, 255)
LARANJA = (255, 204, 0)
CHAO = ALTURA - 150

# Tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Trash Runner")
clock = pygame.time.Clock()

# Carregando fundos
def carregar_fundos(pasta, prefixo):
    fundos = []
    for i in range(1, 5):
        img = pygame.image.load(f"{pasta}/{prefixo}{i}.png").convert()
        img = pygame.transform.scale(img, (LARGURA, ALTURA))
        fundos.append(img)
    return fundos

fundos = carregar_fundos("fundo", "f")
fundos2 = carregar_fundos("fundo2", "fn")
fundos3 = carregar_fundos("fundo3", "fl")
fundos4 = carregar_fundos("fundo4", "flr")
fundos5 = carregar_fundos("fundo5", "fw")

fundo_atual = fundos

# Spritesheet e imagens
spritesheet = pygame.image.load("ps1.png").convert_alpha()
img_game_over = pygame.image.load("game_over.png").convert_alpha()
img_game_over = pygame.transform.scale(img_game_over, (800, 300))
img_lixo = pygame.image.load("coletadolixo.png").convert_alpha()
img_lixo = pygame.transform.scale(img_lixo, (100, 100))

# Sons
som_pulo = pygame.mixer.Sound("pulo-luffy.mp3")
som_morte = pygame.mixer.Sound("aiai_1.mp3")



pygame.mixer.init()
pygame.mixer.music.load('Burn_Rubber.mp3') 
pygame.mixer.music.play(-1, 0.0) 

# Estados do jogo
TELA_INICIAL = 0
JOGANDO = 1
GAME_OVER = 2
TELA_MISSAO = 3
estado_jogo = TELA_INICIAL

vida = 1
pontuacao = 0
score = 0

velocidade_base = 10
multiplicador_velocidade = 1.0

proxima_meta = 1500
passo_meta = 2000
passo_multiplicador = 0.1

nivel_fundo = 1

# Fundo
velocidade_fundo = 5
num_fundos = len(fundos)
posicoes_fundos = [i * LARGURA for i in range(num_fundos)]

# Botões
play_rect = pygame.Rect(LARGURA//2 - 200, 400, 400, 100)
sair_rect = pygame.Rect(LARGURA//2 - 200, 550, 400, 100)
reiniciar_rect = pygame.Rect(LARGURA//2 - 200, 750, 400, 100)
continuar_rect = pygame.Rect(LARGURA//2 - 200, 600, 400, 100)

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
            
class LixoTipo2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lixo2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA + randint(1000, 1400)
        self.rect.y = CHAO - self.rect.height

    def update(self):
        self.rect.x += -velocidade_base * multiplicador_velocidade
        if self.rect.right < 0:
            self.rect.x = LARGURA + randint(1000, 1400)

jogador = Jogador()
obstaculo = Obstaculo()
lixo = Lixo()
todos = pygame.sprite.Group(jogador, obstaculo, lixo)

def desenhar_tela_inicial():
    tela.blit(fundos[0], (0, 0))
    fonte_titulo = pygame.font.SysFont("Arial Black", 140)
    logo = pygame.image.load("Trash_Runner_logo.png").convert_alpha()
    logo = pygame.transform.scale(logo, (800, 190))
    tela.blit(logo, (LARGURA//2 - logo.get_width()//2, 200))
    fonte_botao = pygame.font.SysFont("Arial", 70, bold=True)
    play = fonte_botao.render("PLAY", True, BRANCO)
    sair = fonte_botao.render("SAIR", True, BRANCO)
    logo_unifafire = pygame.image.load("fdwq.png").convert_alpha()
    logo_unifafire = pygame.transform.scale(logo_unifafire, (500, 250))
    tela.blit(logo_unifafire, (LARGURA//2 - logo_unifafire.get_width()//2, sair_rect.bottom + 50))
    pygame.draw.rect(tela, VERDE, play_rect, border_radius=20)
    pygame.draw.rect(tela, VERMELHO, sair_rect, border_radius=20)
    tela.blit(play, (play_rect.centerx - play.get_width()//2, play_rect.y + 15))
    tela.blit(sair, (sair_rect.centerx - sair.get_width()//2, sair_rect.y + 15))
    pygame.display.flip()

def desenhar_game_over():
    tela.blit(fundo_atual[0], (0, 0))
    tela.blit(img_game_over, (LARGURA//2 - img_game_over.get_width()//2, 150))

    fonte_info = pygame.font.SysFont("Arial Black", 80)
    fonte_botao = pygame.font.SysFont("Arial", 70, bold=True)

    # Mostrando Distância e Pontuação
    texto1 = fonte_info.render(f"Distância: {score}", True, VERDE_ESCURO)
    texto2 = fonte_info.render(f"Lixo coletado: {pontuacao}", True, AZUL)

    tela.blit(texto1, (LARGURA // 2 - texto1.get_width() // 2 - 1, 500))
    tela.blit(texto2, (LARGURA // 2 - texto2.get_width() // 2 - 1, 580))

    # texto verde por cima
    texto1_colorido = fonte_info.render(f"Distância: {score}", True, VERDE)
    texto2_colorido = fonte_info.render(f"Lixo coletado: {pontuacao}", True, BRANCO)

    tela.blit(texto1_colorido, (LARGURA // 2 - texto1_colorido.get_width() // 2, 490))
    tela.blit(texto2_colorido, (LARGURA // 2 - texto2_colorido.get_width() // 2, 570))



    reiniciar = fonte_botao.render(" REINICIAR", True, BRANCO)
    pygame.draw.rect(tela, AZUL, reiniciar_rect, border_radius=20)
    tela.blit(reiniciar, (reiniciar_rect.centerx - reiniciar.get_width()//2, reiniciar_rect.y + 15))
    pygame.display.flip()

def desenhar_tela_missao():
    tela.blit(fundo_atual[0], (0, 0))
    fonte_titulo = pygame.font.SysFont("Arial Black", 100)
    texto = fonte_titulo.render("OBRIGADO POR", True, BRANCO)
    texto2 = fonte_titulo.render("COLETAR OS LIXOS!", True, BRANCO)
    tela.blit(texto, (LARGURA//2 - texto.get_width()//2, 250))
    tela.blit(texto2, (LARGURA//2 - texto2.get_width()//2, 400))
    fonte_botao = pygame.font.SysFont("Arial", 60, bold=True)
    continuar = fonte_botao.render("CONTINUAR", True, PRETO)
    pygame.draw.rect(tela, AZUL, continuar_rect, border_radius=70)
    tela.blit(continuar, (continuar_rect.centerx - continuar.get_width()//2, continuar_rect.y + 15))
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
                    nivel_fundo = 1
                    fundo_atual = fundos
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
            pontuacao += 1
            lixo.rect.x = LARGURA + randint(600, 1000)
            
            if pontuacao >= 80 and nivel_fundo < 5:
                fundo_atual = fundos5
                nivel_fundo = 5
                estado_jogo = TELA_MISSAO
            if pontuacao >= 60 and nivel_fundo < 4:
                fundo_atual = fundos4
                nivel_fundo = 4
                estado_jogo = TELA_MISSAO
            elif pontuacao >= 40 and nivel_fundo < 3:
                fundo_atual = fundos3
                nivel_fundo = 3
                estado_jogo = TELA_MISSAO
            elif pontuacao >= 20 and nivel_fundo < 2:
                fundo_atual = fundos2
                nivel_fundo = 2
                estado_jogo = TELA_MISSAO

            if pontuacao % 20 == 0:
                multiplicador_velocidade += 0.5

        for i in range(num_fundos):
            posicoes_fundos[i] -= velocidade_fundo
            if posicoes_fundos[i] <= -LARGURA:
                posicoes_fundos[i] = max(posicoes_fundos) + LARGURA

        for i in range(num_fundos):
            tela.blit(fundo_atual[i], (posicoes_fundos[i], 0))

        todos.draw(tela)

        fonte_info = pygame.font.SysFont("Arial Black", 70)

        tela.blit(fonte_info.render(f"Distância: {score}", True, VERMELHO), (152, 82))
        tela.blit(fonte_info.render(f"{pontuacao}", True, VERMELHO), (272, 182))

        tela.blit(fonte_info.render(f"Distância: {score}", True, PRETO), (151, 81))
        tela.blit(fonte_info.render(f"{pontuacao}", True, PRETO), (271, 181))

        tela.blit(fonte_info.render(f"Distância: {score}", True, LARANJA), (150, 80))
        tela.blit(img_lixo, (150, 180))
        tela.blit(fonte_info.render(f"{pontuacao}", True, LARANJA), (270, 180))

        pygame.display.flip()

    elif estado_jogo == TELA_MISSAO:
        desenhar_tela_missao()
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            elif evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                if continuar_rect.collidepoint(evento.pos):
                    estado_jogo = JOGANDO

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
                    nivel_fundo = 1
                    fundo_atual = fundos
                    estado_jogo = JOGANDO
