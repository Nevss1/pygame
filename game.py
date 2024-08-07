import pygame
from random import randint
pygame.init()
clock = pygame.time.Clock()


# tela
janela = pygame.display.set_mode((1024, 626))
pygame.display.set_caption("Plants vs Zombies")
fundo = pygame.image.load("images/background.png")

# imagens
imagem_cursor = pygame.image.load("images/aim_cursor.png")
imagem_cursor = pygame.transform.smoothscale(imagem_cursor, (384*1.3, 384*1.3))  # define o tamanho do cursor
pygame.mouse.set_visible(False)
wave_4 = pygame.image.load("images/wave4.png")
scale_x, scale_y = wave_4.get_size()
wave_4 = pygame.transform.smoothscale(wave_4, (scale_x*1.5, scale_y*1.5))
zombies_ate_your_brains = pygame.image.load("images/the zombies ate your brains!.png")

# sons
pygame.mixer.music.load("songs/Loonboon.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)
som_tiro = pygame.mixer.Sound("songs/shoot.mp3")
they_are_coming = pygame.mixer.Sound("songs/The Zombies Are coming Sound effect.mp3")
they_are_coming.set_volume(0.5)
zombies_are_coming = True
zombie_death_song = pygame.mixer.Sound("songs/zombie death.mp3")
zombie_death_song.set_volume(0.5)
dying_song = pygame.mixer.Sound("songs/dying song.mp3")
dying_song.set_volume(0.5)

# cone_zombie png
cone_zombie = pygame.image.load("images/zombie1.png")
cz_x, cz_y = cone_zombie.get_size()
cone_zombie = pygame.transform.smoothscale(cone_zombie, (cz_x*0.3, cz_y*0.3))
cone_zombie = pygame.transform.flip(cone_zombie, True, False)  # gira em torno do eixo X

# baby_zombie png
baby_zombie = pygame.image.load("images/baby zombie.png")
bx_z, by_z = baby_zombie.get_size()
baby_zombie = pygame.transform.smoothscale(baby_zombie, (bx_z*0.15, by_z*0.15))

# yeti_zombie png
yeti_zombie = pygame.image.load("images/yetizombie.png")
yz_x, yz_y = yeti_zombie.get_size()
yeti_zombie = pygame.transform.smoothscale(yeti_zombie, (yz_x * 0.1, yz_y * 0.1))

# boss_zombie png
boss_zombie = pygame.image.load("images/bosszombie.png")
bz_x, bz_y = boss_zombie.get_size()

lista_img_zumbis = [cone_zombie, baby_zombie, yeti_zombie, boss_zombie]

# dicionário para imagem dos zumbis
dic_zombies = {"cone_zombie": 0,
               "baby_zombie": 1,
               "yeti_zombie": 2,
               "boss_zombie": 3}

# wave text
pygame.font.init()
fonte = pygame.font.Font("images/SpecialElite-Regular.ttf", 56)
wave1_text = fonte.render("WAVE 1", True, "white")
wave2_text = fonte.render("WAVE 2", True, "white")
wave3_text = fonte.render("WAVE 3", True, "white")
wave5_text = fonte.render("FINAL BOSS IS COMING", True, "red")


class Zombie:
    def __init__(self, x, y, type_zombie, velocidade):
        self.type_zombie = dic_zombies[type_zombie]
        self.imagem = lista_img_zumbis[self.type_zombie]
        # x e y é a posição do zumbi e a área dele
        self.rect = self.imagem.get_rect(topright=(x, y))
        self.velocidade = velocidade
        if self.imagem == cone_zombie:
            self.vida = 1
        if self.imagem == baby_zombie:
            self.vida = 1
        elif self.imagem == yeti_zombie:
            self.vida = 2
        elif self.imagem == boss_zombie:
            self.vida = 6

    def update(self, end_game):  # movimentação
        if not end_game:
            self.rect.x -= self.velocidade

    def draw(self, surface, mouse_pos, raio_visao):
        # define a região da área do zumbi
        rect_visor = pygame.Rect(mouse_pos[0] - raio_visao, mouse_pos[1] - raio_visao, 2 * raio_visao, 2 * raio_visao)
        if self.rect.colliderect(rect_visor):
            surface.blit(self.imagem, self.rect)


# determinação das waves
def wave_turn(txt_wave):
    pos_txt = (500, 260)
    if txt_wave == wave5_text:
        pos_txt = (300, 260)  # alinhamento
    janela.blit(txt_wave, pos_txt)


def tempo_de_spawn(intervalo):
    pygame.time.set_timer(spawn_zumbi_event, intervalo)


# criação dos zumbis
def adicionarzumbi(posy_zombie, type_zombie, velocidade):
    posx_zombie = 905
    if type_zombie == "baby_zombie":
        posy_zombie += 50  # alinhamento da posição do baby_zombie
    elif type_zombie == "boss_zombie":
        posx_zombie += 150

    return Zombie(posx_zombie, posy_zombie, type_zombie, velocidade)


inicial_pos = [15, 100, 200, 300, 400]  # posições Y iniciais dos zumbis
zumbis_vivos = []

# evento personalizado spawn dos zumbis
spawn_zumbi_event = pygame.USEREVENT


def criar_mascara_visao(mouse_pos, raio):
    mascara = pygame.Surface(janela.get_size(), flags=pygame.SRCALPHA)  # cria superfície de canal alfa
    mascara.fill((0, 0, 0, 200))  # máscara fundo preto, o 200 é a escala de transparencia
    pygame.draw.circle(mascara, (0, 0, 0, 0), mouse_pos, raio)  # círculo visível ao redor do mouse
    return mascara


# parâmetros iniciais
tempo_de_spawn(5000)  # start do game
ultimo_tiro = 0  # tempo suporte para recarga do tiro
boss = False
game_over = False  # caso o zumbi chegue no final
end_song = False
game = True

# tela de espera para começar o jogo
tela_espera = True
press_to_start = fonte.render("Press any key to start", True, "white")
while tela_espera:
    janela.blit(fundo, (0, 0))
    janela.blit(press_to_start, (300, 200))

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            tela_espera = False


while game:
    # the_zombies_are_coming song
    if zombies_are_coming:
        they_are_coming.play()
        zombies_are_coming = False

    janela.blit(fundo, (0, 0))
    tempo_atual = pygame.time.get_ticks()  # tempo percorrido do jogo

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if tempo_atual - ultimo_tiro > 2000:  # 2s tempo de recarga
                som_tiro.play()
                pos_click = event.pos  # tupla posição do mouse
                ultimo_tiro = tempo_atual
                # verifica se algum zumbi da lista foi atingido
                for zumbi in zumbis_vivos:
                    area_zumbi = zumbi.imagem.get_rect(topleft=[zumbi.rect.x, zumbi.rect.y])  # rect do zumbi
                    if area_zumbi.collidepoint(pos_click):
                        zumbi.vida -= 1
                        if zumbi.vida == 0:
                            zumbis_vivos.remove(zumbi)
                            zombie_death_song.play()
                        break
                # recoil
                pygame.mouse.set_pos(pos_click[0], pos_click[1]-30)

        # evento personalizado para spawn aleatório de zumbis a cada intervalo
        elif event.type == spawn_zumbi_event:
            random = randint(0, 4)
            if tempo_atual < 33000:  # timer da wave 1
                # parâmetros: posição inicial, tipo do zumbi, velocidade
                zumbis_vivos.append(adicionarzumbi(inicial_pos[random], "cone_zombie", 4))
                # spawn de zumbi a cada 2 segundos
                tempo_de_spawn(2500)

            elif 35000 < tempo_atual < 52000:  # timer da wave 2
                zumbis_vivos.append(adicionarzumbi(inicial_pos[random], "baby_zombie", 2.8))
                tempo_de_spawn(3000)

            elif 55000 < tempo_atual < 75000:  # timer da wave 3
                zumbis_vivos.append(adicionarzumbi(inicial_pos[random], "yeti_zombie", 1))
                tempo_de_spawn(4500)

            elif 80000 < tempo_atual < 100000:  # timer da wave 4
                random2 = randint(0, 4)
                zumbis_vivos.append(adicionarzumbi(inicial_pos[random], "yeti_zombie", 1))
                zumbis_vivos.append(adicionarzumbi(inicial_pos[random2], "cone_zombie", 1.5))
                tempo_de_spawn(5500)

            elif tempo_atual > 105000:  # final boss
                if not boss:
                    zumbis_vivos.append(adicionarzumbi(inicial_pos[1], "boss_zombie", 0.8))
                boss = True
    # atualização dos zumbis
    pos_mouse = pygame.mouse.get_pos()
    for zumbi in zumbis_vivos:
        zumbi.update(game_over)  # movimenta o zumbi
        zumbi.draw(janela, pos_mouse, 130)  # desenha o zumbi
        if zumbi.rect.x <= 150 and zumbi.type_zombie != 3:
            game_over = True  # fim de jogo
        elif zumbi.rect.x <= 0 and zumbi.type_zombie == 3:  # 3 é o boss_zombie
            game_over = True

    # máscara de visão para círculo de mira
    mascara_visao = criar_mascara_visao(pos_mouse, 180)
    janela.blit(mascara_visao, (0, 0))

    # cursor de mira
    x_mouse, y_mouse = pygame.mouse.get_pos()
    pos_cursor = [x_mouse-250, y_mouse-250]  # centraliza o png
    janela.blit(imagem_cursor, pos_cursor)  # atualiza o novo cursor

    # texto das waves
    if not game_over:
        if tempo_atual < 4000:
            wave_turn(wave1_text)
        elif 35000 < tempo_atual < 40000:
            wave_turn(wave2_text)
        elif 55000 < tempo_atual < 60000:
            wave_turn(wave3_text)
        elif 80000 < tempo_atual < 84000:
            janela.blit(wave_4, (120, -50))  # a huge wave of zombies png
        elif 105000 < tempo_atual < 110000:
            wave_turn(wave5_text)

    if game_over:
        janela.blit(zombies_ate_your_brains, (300, 60))
        if not end_song:
            dying_song.play()
            end_song = True
        for zombie in zumbis_vivos:
            if zombie.rect.x >= 155:
                zumbis_vivos.remove(zombie)
                pygame.mixer.music.stop()

        pygame.display.flip()

    clock.tick(45)
    pygame.display.flip()

pygame.quit()
