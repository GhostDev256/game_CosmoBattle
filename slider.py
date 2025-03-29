from pygame import mixer, transform, image
from time import time as t
from config import *
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

#from os import listdir, path

class Slider:
    def __init__(self, slider, knob, wh, pos): # wh - (Ширина, Высота)
        self.volume = 1
        self.pos = pos
        self.slider = transform.scale(image.load(slider).convert_alpha(), wh)
        self.knob = transform.scale(image.load(slider).convert_alpha(), (20, wh[1]))

        self.slider_rect = self.slider.get_rect()
        self.knob_rect = self.knob.get_rect()

        self.slider_rect.x, self.slider_rect.y = self.pos
        self.knob_rect.x, self.knob_rect.y = self.pos
        self.knob_rect.x += wh[0]-20

        self.dragging = False

        # Ладно, устал. Пора спать (Ночь 17.10.2024)
        # (Спустя пару часов) А хуй я посплю, продолжим еблю.

    def render_slider(self, screen):
        screen.blit(self.slider, self.slider_rect)
        screen.blit(self.knob, self.knob_rect)

    def event_slider(self, event):
        # Обработка нажатия на ползунок
        if event.type == MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(event.pos):
                self.dragging = True

        # Обработка отпускания кнопки мыши
        if event.type == MOUSEBUTTONUP:
            self.dragging = False

        # Перемещение ползунка при движении мыши
        if event.type == MOUSEMOTION and self.dragging:
            self.knob_rect.x = max(self.slider_rect.x, min(event.pos[0] - self.knob_rect.width // 2, self.slider_rect.right - self.knob_rect.width))

            # Рассчёт громкости на основе положения ползунка
            self.volume = (self.knob_rect.x - self.slider_rect.x) / (self.slider_rect.width - self.knob_rect.width)

        return self.volume