from pygame import Surface, image, mixer, transform, key, time
from gameobject import GameObject
from os import listdir, path
from config import GUN, BUL, GUNFIRESOUND, PLASMAGUN, PLASMA, BASEBUL, BASEPLASMA, LASERGUN, LASER, BASELASER, INVENTORY
from bullet import Bullet
from time import time as t

class Ship(GameObject):
    def __init__(self, size_w, size_h, speed, screen, img, pos, xp=100, destruction_sound=None, rotate=0):
        GameObject.__init__(self, size_w, size_h, speed, screen, img, pos, xp, destruction_sound)

        self.alife = True
        self.xp = xp
        #self.img_fire = img_fire
        self.rotate = rotate
        if self.rotate == 180:
            self.direct_bullet = -1
        else:
            self.direct_bullet = 1

        self.start_time_fire = t()
        self.current_gun = 'лазер'  
        #self.bullet = self.current_gun
        #self.current_bul = Bullet(10, 10, 15, self.screen, BUL, pos=(self.rect.x + 25, self.rect.y))
        self.activ_gun()
        
    def anim_fire(self):        
        if not self.start_anim_dead:
            self.screen.blit(self.animation_fire[self.frame_anim], (self.rect.x, self.rect.y))
            
            if self.start_anim_fire:
                self.frame_anim += 1

                if self.frame_anim == len(self.animation_fire):
                    self.start_anim_fire = False
                    self.frame_anim = 0
                elif self.frame_anim == 1:
                    self.fire_sound.play()

    def change_activ_gun(self, new): # Чтобы переключаться во время игры
        '''
        пушка\n
        плазма\n
        лазер\n
        ракеты (pass)
        '''
        self.current_gun = new
        self.activ_gun()

    def change_gun(self, img_gun, fire_sound):
        self.fire_sound = mixer.Sound(path.join(GUNFIRESOUND, fire_sound))
        self.fire_sound.set_volume(0.35)

        self.animation_fire.clear()
        for i in listdir(img_gun):
            self.animation_fire.append(transform.rotate(transform.scale(image.load(path.join(img_gun, i)).convert_alpha(), (self.size_w, self.size_h)), self.rotate))

    def activ_gun(self): # На будущее (Сделано. Ну, почти.)
        if self.current_gun == 'пушка':
            self.change_gun(GUN, 'gun_fire_sound.wav')
            self.bullet = (10, 10, 15, BASEBUL, BUL, 25 + (5 * INVENTORY['improvements']['damage']))
            self.cooldown_fire = 0.7
        elif self.current_gun == 'плазма':
            self.change_gun(PLASMAGUN, 'plasma_fire_sound.mp3')
            self.bullet = (22, 22, 8, BASEPLASMA, PLASMA, 100 + (20 * INVENTORY['improvements']['damage']))
            self.cooldown_fire = 3
        elif self.current_gun == 'лазер':
            self.change_gun(LASERGUN, 'laser_fire_sound.mp3')
            self.bullet = (12, 32, 32, BASELASER, LASER, 50 + (10 * INVENTORY['improvements']['damage']))
            self.cooldown_fire = 2
        elif self.current_gun == 'ракеты':
            pass

    def fire(self, anim=True):
        if t() - self.start_time_fire > self.cooldown_fire:
            if anim:
                self.start_anim_fire = True
            self.start_time_fire = t()

            return Bullet(self.bullet[0], self.bullet[1], self.bullet[2]*self.direct_bullet, self.screen, self.bullet[3], self.bullet[4], pos=(self.rect.x + 22, self.rect.y), damage=self.bullet[5])