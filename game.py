from pygame import (image, transform, key,
                    init, mixer, font, display, 
                    time, event)

from pygame.locals import *
from config import *
from mainmenu import MainMenu

from os import listdir, path

class Game(MainMenu):
    def __init__(self, game_name = 'Что-то'):      
        init()
        mixer.init()
        font.init()
        display.set_caption(game_name)

        self.screen = display.set_mode((W, H))
        MainMenu.__init__(self, self.screen)

        self.clock = time.Clock()
        self.obj = []
        self.GAME_POINT = 0
        self.play = True # Игровой цикл в Main
        
        self.bg_game = transform.scale(image.load(BG_GAME).convert(), (W, H))
        self.bg_menu = transform.scale(image.load(BG_MENU).convert(), (W, H))
        self.bg_y = 0
        
        self.font = font.SysFont('Times New Roman', 32)

        self.reload_sound(MENUGAMESOUND) 
        self.player_xp = 100 + (10 * INVENTORY['improvements']['healf'])

    def draw_dot(self, img, pos):
        self.screen.blit(transform.scale(image.load(img), (15, 30)), pos)

    def draw_bar(self, img_bar, img_dot, volume, pos=(W/2, 50)):
        self.screen.blit(transform.scale(image.load(img_bar), (180, 40)), pos)

        dot = self.player_xp/10
        """print('------------')
        print(f'Здоровье (факт): {volume}')
        print(f'Здоровье: {self.player_xp}')
        print(f'1 бар: {dot}')
        print(f'Кол-во баров: {volume/dot}')"""

        for i in range(round(volume/dot)):
            self.draw_dot(img_dot, ((pos[0] + 152) - 15 * (i + 1), pos[1]+5))

    def draw_bg(self, bg_img, speed=2):
        self.screen.blit(bg_img, (0, self.bg_y))
        self.screen.blit(bg_img, (0, self.bg_y + H))

        self.bg_y -= speed
        if self.bg_y <= -H:
            self.bg_y = 0

    def pause(self):
        paused = True
        while paused:
            events = event.get()

            for game_event in events:
                if game_event.type == QUIT:
                    quit()
                if game_event.type == KEYDOWN:
                    if game_event.key == K_q:
                        paused = False 

            self.text_title('Пауза!')
            self.text_title('Нажмите "Q", чтобы продолжить', pos=(W/2, H/2 + 40))

            display.update()
            self.clock.tick(15)