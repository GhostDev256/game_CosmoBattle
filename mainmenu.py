from pygame import display, time, font, mixer, mouse, transform, image
from pygame.locals import *
from time import time as t
from config import *
from buttom import Button
from slider import Slider

from os import listdir, path

class MainMenu():
    def __init__(self, screen):
        self.screen = screen
        font.init()
        
        self.font = font.SysFont('Times New Roman', 48)
        self.small_font = font.SysFont('Times New Roman', 24)

        self.windows = {
            'menu': {
                'action': True,
                'UI_function': self.draw_menu,
                'button': [Button('Играть', (70, 180), action=self.play_game),
                           Button('Магазин', (70, 255), action=self.click_shop),
                           Button('Настройки', (70, 330), action=self.click_setting),
                           Button('Выйти', (70, 405), action=self.exit_game)
                          ],
            },
            'settings': {
                'action': False,
                'UI_function': self.draw_settings,
                'button': [Button('Назад', (W/2 - 105, 530), action=self.click_back)]
            },
            'shop': {
                'action': False,
                'UI_function': self.draw_shop,
                'button': [Button('Назад', (W/2 - 105, 620), action=self.click_back),
                           Button('Купить', (W/2 - 495, 160), id_button=6),
                           Button('Купить', (W/2 - 495, 240), id_button=7),
                           Button('Купить', (W/2 - 495, 320), id_button=8),
                           Button('Купить', (W/2 - 495, 400), id_button=9),
                           Button('Купить', (W/2 - 495, 480), id_button=5)
                           ]     
            }
        }

        self.activ_button = 0
        self.music_volume = 0.7
        self.buttons = []
        self.slider_music = Slider(SCROLLBAR, KNOB, (200, 40), (560, 185)) # Бля, какой же костыль...нужно будет сделать
                                                                           # Окошки и виджеты нормальные.

        for i in self.windows:
            self.buttons.append(self.windows[i]['button'])
        
        self.running = False
        self.activ_but_sound = True

    def draw_button(self, buttons):
        '''Отрисовать кнопки'''
        for button in buttons:
            self.screen.blit(button.icon, button.rect)

            text_surf = self.font.render(button.text, True, WHITE)
            text_rect = text_surf.get_rect(center=button.rect.center)
            self.screen.blit(text_surf, text_rect)

    def draw_settings(self):
        self.win = transform.scale(image.load(WINDOW).convert_alpha(), (500, 500))
        self.screen.blit(self.win, (W/2 - 250, 100))  
        self.draw_button(self.windows['settings']['button'])
        self.text_title('Музыка:', pos=(490, 200))

        self.slider_music.render_slider(self.screen)
    
    def draw_menu(self):
        self.win = transform.scale(image.load(WINDOW).convert_alpha(), (250, 470))
        self.screen.blit(self.win, (50, 100))  
        self.draw_button(self.windows['menu']['button'])

    def draw_shop(self):
        self.win = transform.scale(image.load(WINDOW).convert_alpha(), (1100, 660))
        self.screen.blit(self.win, (W/2 - 550, 50))  
        #self.text_title('Магазин в разработке', pos=(550, 200))
        self.draw_button(self.windows['shop']['button'])

        if self.activ_button != 0:
            for i in INVENTORY:
                if OBJECT_ID[self.activ_button] in INVENTORY[i].keys():
                    INVENTORY[i][OBJECT_ID[self.activ_button]] = INVENTORY[i][OBJECT_ID[self.activ_button]] + 1
                    print(INVENTORY[i])
                    self.activ_button = 0
            
    def click_setting(self):
        self.change_activ_window('settings')
    def click_shop(self):
        self.change_activ_window('shop')
    def click_back(self):
        self.change_activ_window('menu')

    def change_activ_window(self, activ): 
        '''Изменить активное окно'''
        for win in self.windows:
            if activ == win:
                self.windows[win]['action'] = True # Не забыть изменить (Переделал)
            else:
                self.windows[win]['action'] = False 

    def window_manager(self):
        '''Управление окнами'''
        for window in self.windows:
            if self.windows[window]['action']:
                self.windows[window]['UI_function']()

    def handle_event(self, event):
        '''Обработка нажатия на кнопи'''
        for win in self.windows:
            if self.windows[win]['action']:
                for button in self.windows[win]['button']:
                    is_hovered = button.rect.collidepoint(mouse.get_pos())
                    
                    # Проверяем, было ли уже наведено на кнопку
                    if is_hovered and not button.hovered:
                        button.press_sound.play()
                        button.change_icon(PRESS_BUTTONICON)
                        button.hovered = True  # Помечаем кнопку как "подсвеченную"
                    elif not is_hovered:
                        button.change_icon(BASE_BUTTONICON)
                        button.hovered= False  # Сбрасываем состояние при уходе с кнопки

                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        if is_hovered:
                            self.activ_button = button.id_button
                            print(self.activ_button)

                            button.click_sound.play()
                            button.change_icon(CLICK_BUTTONICON)
                            button.connect()

        if self.windows['settings']['action']:
            mixer.music.set_volume(self.slider_music.event_slider(event))
    
    def play_game(self):
        '''
        Начало игры\n
        Изменяет значение свойства self.running на True
        '''
        print('Начинаем игру...')  
        
        countdown = 4  # Отсчёт времени до начала игры
        while countdown > 1:
            countdown -= 1
            self.screen.fill(BLACK)
            countdown_text = self.font.render(f'Игра начнется через: {countdown}', True, WHITE)
            self.screen.blit(countdown_text, (200, 200))
            display.update()
            time.wait(1000)
        else:
            self.running = True
            self.reload_sound(GAMESOUND)

    def exit_game(self):
        print('Игра завершена.')
        quit()

    def reload_sound(self, sound):
        for i in listdir(sound):
            mixer.music.load(path.join(sound, i))
            
        mixer.music.play(loops=-1)

    def text_title(self, txt='Надпись', color=(255, 255, 255), pos=(W/2, H/2)):
        '''Сделать надпись'''
        text = self.font.render(str(txt), True, color)
        text_rect = text.get_rect(center=pos)
        self.screen.blit(text, text_rect)

