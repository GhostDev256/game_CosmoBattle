from pygame import Surface, image, transform, key, sprite, draw, Rect, mask, mixer
from config import *

from os import listdir, path

class GameObject(sprite.Sprite):
    def __init__(self, size_w, size_h, speed, screen: Surface, img=None, pos=(150, 150), xp = 100, destruction_sound=None, img_fire=None): # wh - ширина/высота
        sprite.Sprite.__init__(self)
        
        self.pos = pos
        self.size_w = size_w
        self.size_h = size_h
        self.speed = speed
        self.screen = screen     
        self.xp = xp
        if destruction_sound:
            self.destruction_sound = mixer.Sound(destruction_sound)

        if img is None:    
            self.image = Surface((size_w, size_h))
            self.rect = self.image.get_rect(center=self.pos)
            self.image.fill((100, 0, 0))
        else:
            self.image = image.load(img).convert_alpha()
            self.image = transform.scale(self.image, (self.size_w, self.size_h))
            self.rect = self.image.get_rect() # width=collize_wh[0], height=collize_wh[1]
            self.rect.x, self.rect.y = (self.pos[0], self.pos[1])

        self.last_rect_x = self.rect.x
        self.last_rect_y = self.rect.y

        self.mask = mask.from_surface(self.image)
        self.anim_dead = []
        self.animation_fire = []
        self.frame_anim = 0
        self.start_anim_fire = False
        self.start_anim_dead = False

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))  
        #print(self.rect.x, self.rect.y)

    def animation(self, anim, dead=True):
        '''
        anim - список с анимацией\n
        dead - нужно ли уничтожать обьект после первого лупа анимации
        '''
        try:
            self.image = anim[self.frame_anim]
            self.frame_anim += 1
        except:
            print('ОШИБКА')
            print('Длина:', len(anim))
            print('Спискок:', anim)
            print('Фрейм:', self.frame_anim)

        if len(anim) == self.frame_anim and dead:
            self.kill()
        elif len(anim) == self.frame_anim and not dead:
            self.frame_anim = 0

    '''
    def move(self):
        pass
    '''