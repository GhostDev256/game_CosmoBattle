from pygame import Surface, image, transform, key, draw
from gameobject import GameObject
from os import listdir, path

from config import H

class Bullet(GameObject):
    '''Пулька, Ы'''
    def __init__(self, size_w, size_h, speed, screen: Surface, img=None, anim_img=None, pos=(0, 0), damage=40):
        GameObject.__init__(self, size_w, size_h, speed, screen, img, pos)
        
        self.damage = damage

        if anim_img:
            for i in listdir(anim_img):
                self.animation_fire.append(transform.scale(image.load(path.join(anim_img, i)).convert_alpha(), (self.size_w, self.size_h)))
            
            self.start_anim_fire = True

    def update(self):
        if self.rect.y < H:
            self.rect.move_ip(0, -self.speed)
            if self.start_anim_fire:
                self.animation(self.animation_fire, dead=False)
        else:
            self.kill()