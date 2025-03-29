from pygame import mixer, transform, image
from time import time as t
from config import *

from os import listdir, path
mixer.init()

class Button:
    def __init__(self, text, pos, wh=(210, 45), icon=BASE_BUTTONICON, hovered=False, 
                 press_sound=mixer.Sound(PRESS_BUTTONSOUND), 
                 click_sound=mixer.Sound(CLICK_BUTTONSOUND),
                 action=None, id_button=0):
        
        self.id_button = id_button
        self.text = text
        self.pos = pos
        self.wh = wh # ширина/высота
        self.icon = transform.scale(image.load(icon).convert_alpha(), wh)
        self.hovered = hovered
        self.press_sound = press_sound
        self.click_sound = click_sound
        self.action = action

        self.rect = self.icon.get_rect()
        self.rect.x, self.rect.y = self.pos

    def connect(self):
        if self.action:
            self.action()

    def get_id(self):
        return self.id_button

    def change_icon(self, new_icon):
        self.icon = transform.scale(image.load(new_icon).convert_alpha(), self.wh)