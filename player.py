from pygame import key
from pygame.locals import *
from time import time as t
from ship import Ship
from config import W, H

class Player(Ship):
    def __init__(self, size_w, size_h, speed, screen, img, pos, xp=100, destruction_sound=None):
        Ship.__init__(self, size_w, size_h, speed, screen, img, pos, destruction_sound)

        self.xp = xp
        
        self.start_time_fire = t()
        self.current_gun = 'лазер'  
    
    def move(self):
        self.last_rect_x = self.rect.x
        self.last_rect_y = self.rect.y
        
        keys = key.get_pressed()
        if (keys[K_a] or keys[K_LEFT]) and self.rect.x > 5:
            self.rect.move_ip(-self.speed, 0)
        if (keys[K_d] or keys[K_RIGHT]) and self.rect.x < W - 5 - self.size_w:
            self.rect.move_ip(self.speed, 0)
        if (keys[K_w] or keys[K_UP]) and self.rect.y > 5:
            self.rect.move_ip(0, -self.speed)
        if (keys[K_s] or keys[K_DOWN]) and self.rect.y < H - 5 - self.size_h:
            self.rect.move_ip(0, self.speed)