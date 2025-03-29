from pygame import Surface, image, transform, key, mixer, draw
from gameobject import GameObject
from os import listdir, path
from config import ASTEROID, ASTEROIDANIM, ASTEROIDDESTRUCTSOUND, H

class Asteroid(GameObject):
    '''Камушек, Ы'''
    def __init__(self, size_w, size_h, speed, screen: Surface, img=None, pos=(0, 0), xp = 150, destruction_sound=ASTEROIDDESTRUCTSOUND):
        GameObject.__init__(self, size_w, size_h, speed, screen, img, pos, xp, destruction_sound) # asteroid_destruction.wav

        self.damage = 150

        for i in listdir(ASTEROIDANIM):
            self.anim_dead.append(transform.scale(image.load(path.join(ASTEROIDANIM, i)).convert_alpha(), (size_w, size_h)))

        #self.exists = True

    def update(self):
        if self.start_anim_dead:
            self.animation(self.anim_dead)
            self.mask.clear()
        elif self.rect.y < H+20:
            self.rect.y += self.speed
        else:
            self.kill()

'''    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        draw.rect(self.screen, (255, 0, 0), self.rect)'''