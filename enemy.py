# Я СДЕЛАЛ ЭТО! СДЕЛАЛ!!

from pygame import sprite, image, transform, Surface
from gameobject import GameObject
from config import ENEMY, W, H, ENEMYANIM, ASTEROIDDESTRUCTSOUND
from random import randint
from ship import Ship
from bullet import Bullet
from os import listdir, path

# Больше, мать его, никогда В ЖИЗНИ!
class Enemy(Ship):
    def __init__(self, size_w, size_h, speed, screen: Surface, 
                 img=ENEMY, pos=(150, 150), xp=50, 
                 fire_sound='player_fire_sound.wav', 
                 destruction_sound=ASTEROIDDESTRUCTSOUND, 
                 img_fire=None, rotate=180):
        
        Ship.__init__(self, size_w, size_h, speed, screen, img, pos, xp, destruction_sound, rotate=rotate)
        
        self.image = transform.rotate(self.image, rotate)
        self.rect.center = self.pos
        self.cooldown = 20

        self.base_follow_distance = randint(200, 350) # Базовое расстояние для игрока
        self.dead_zone = randint(50, 80) # Радиус мёртвой зоны
        self.min_bot_distance = 100  # Минимальное расстояние между ботами
        self.retreating = False # Режим отступления
        self.attack = False # Разрешение на атаку

        self.danger_vector = [0, 0] # Вектор уклонения
        self.cooldown_retreating = 0
        self.valuse_cooldown_retreating = 7 # Как долго боту нужно ждать после появления угрозы
                                            # Нужно, чтобы боты не дрыгались туда-сюда в ситуациях:
                                            # 1. Летим к игроку, камень - от камня 2. Летим к игроку, камень - от камня 3. Летим к игроку, камень - от камня. и т.д.

        for i in listdir(ENEMYANIM):
            self.anim_dead.append(transform.rotate(transform.scale(
                image.load(path.join(ENEMYANIM, i)).convert_alpha(),
                (size_w, size_h)), rotate))

    def avoid_threats(self, asteroids, player_bullets):
        """
        Уклонение от угроз\n
        Возвращает False, если угроз нету и True, если уклоняется прямо сейчас
        """
        
        # От пуль
        for bullet in player_bullets:
            if abs(self.rect.x - bullet.rect.x) < 60 and 0 < bullet.rect.y - self.rect.y < 100:
                if self.rect.centerx < bullet.rect.centerx:
                    self.danger_vector[0] = self.speed
                else:
                    self.danger_vector[0] = self.speed

                if abs(self.rect.x - bullet.rect.x) < 30:
                    self.danger_vector[1] = self.speed

        # От астероидов
        for asteroid in asteroids:
            if abs(self.rect.x - asteroid.rect.x) < 50 and abs(self.rect.y - asteroid.rect.y) < 60:
                if self.rect.centerx < asteroid.rect.centerx:
                    self.danger_vector[0] = self.speed
                else:
                    self.danger_vector[0] = self.speed

                if abs(self.rect.y - asteroid.rect.y) < 50:
                    self.danger_vector[1] = self.speed

        # Уклоняемся
        if self.danger_vector != [0, 0]:
            self.rect.x += self.danger_vector[0]
            self.rect.y += self.danger_vector[1]

            self.danger_vector[0] = 0
            self.danger_vector[1] = 0
            self.cooldown_retreating = self.valuse_cooldown_retreating
            return True  
        
        return False

    def avoid_other_bots(self, enemy_group):
        """Избегаем других ботов"""
        for other_bot in enemy_group:
            if other_bot == self:
                continue

            dx = self.rect.centerx - other_bot.rect.centerx
            dy = self.rect.centery - other_bot.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance < self.min_bot_distance:
                if dx > 0:
                    self.rect.x += int(self.speed / 2)
                else:
                    self.rect.x -= int(self.speed / 2)

                if dy > 0:
                    self.rect.y += int(self.speed / 2)
                else:
                    self.rect.y -= int(self.speed / 2)

    # Какой заёб, я манал...
    def retreat_after_attack(self):
        """Отступление после атаки."""
        if not hasattr(self, 'retreat_target') or self.retreat_target is None:
            retreat_x = self.rect.centerx + randint(-150, 150)
            retreat_y = self.rect.centery + randint(-70, 50)
            self.retreat_target = (retreat_x, retreat_y)

        dx = self.retreat_target[0] - self.rect.centerx
        dy = self.retreat_target[1] - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < 10:  
            self.retreat_target = None
            if self.cooldown == 0:
                self.retreating = False
        else:
            '''if self.rect.left < 0:  # Левая граница
                self.rect.left = 0
                dx *= -1
            elif self.rect.right > self.screen.get_width():  # Правая граница
                self.rect.right = self.screen.get_width()
                dx *= -1
            else:'''
            # Двигаемся к целевой точке
            self.rect.x += self.speed * (dx / distance)
            self.rect.y += self.speed * (dy / distance)

    def follow_player(self, player):
        """Преследование игрока"""
        dx = player.rect.centerx + 70 - self.rect.centerx
        dy = player.rect.centery + 70 - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if self.rect.centery + 150 > player.rect.centery: # В 150 пикселях над игроком
            self.rect.y -= self.speed
        elif distance > self.base_follow_distance + self.dead_zone:
            self.rect.x += self.speed * (dx / distance)
            self.rect.y += self.speed * (dy / distance)
        elif distance < self.base_follow_distance - self.dead_zone:
            self.rect.x -= self.speed * (dx / distance)
            self.rect.y -= self.speed * (dy / distance)
        else:
            self.attack = True

    def align_to_attack(self, player):
        """Выход на вектор атаки"""
        if self.cooldown > 0:  
            return

        dx = player.rect.centerx - self.rect.centerx

        if abs(dx) < 15:
            return
        
        if self.rect.centery + 150 > player.rect.centery: # В 150 пикселях над игроком
            self.rect.y -= self.speed

        if dx > 0:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def can_shoot_player(self, player):
        """Проверка на возможность атаки (Нужно ли стрелять именно сейчас)"""
        return abs(self.rect.centerx - player.rect.centerx) < 15 and player.rect.centery + 150 > self.rect.centery

    def shoot(self, bot_bullet_group, player):
        """Стреляем"""
        if self.cooldown == 0 and self.can_shoot_player(player):
            bul = self.fire()
            if bul:
                bot_bullet_group.add(bul)
                self.cooldown = 40
                self.attack = False
            else:
                self.cooldown = 40
                self.attack = False

    '''
    def adjust_follow_distance(self, player):
        player_speed = abs(player.rect.x - player.last_rect_x) + abs(player.rect.y - player.last_rect_y)
        self.follow_distance = self.base_follow_distance + player_speed * 10

        
    def limit_movement(self):
        """Ограничение перемещения ботов"""
        
    '''

    def update(self, asteroids, player_bullets, bot_bullet_group, enemy_group, player):
        if self.start_anim_dead:
            self.animation(self.anim_dead)
        elif self.rect.y > H + 20:
            self.mask.clear()
            self.kill()
        else:
            if self.avoid_threats(asteroids, player_bullets):
                pass
            else:
                if not self.cooldown_retreating > 0:
                    #self.adjust_follow_distance(player)
                    self.avoid_other_bots(enemy_group)

                    if hasattr(self, 'retreating') and self.retreating: 
                        self.retreat_after_attack()
                    else:
                        if self.attack:    
                            self.align_to_attack(player)
                            if self.can_shoot_player(player):
                                self.shoot(bot_bullet_group, player)
                                self.retreating = True  
                        else: 
                            self.follow_player(player)

            if self.cooldown > 0:
                self.cooldown -= 1
            if self.cooldown_retreating > 0:
                self.cooldown_retreating -= 1