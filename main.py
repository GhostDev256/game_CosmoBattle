'''
Список дел:

+ 1. Добавить фон (сделать его двигающимся +) #25.09.2024
+ 2. Добавить игрока #25.09.2024
+ 3. Добавить астероиды #9.10.2024
+ 4. Добавить пушку для игрока и возможность стрелять #25.09.2024
+ 5. Добавть анимацию стрельбы #2.10.2024
+ 6. Анимация разрушения астероида #16.10.2024
+ 7.1 Найти звуки стрельбы, разрушения и т.д. #25.09.2024
+ 7.2 Добавить звуки стрельбы, разрушения и т.д. #16.10.2024
+ 8.1 Добавить хп для игрока #16.10.2024
+ 8.2 Столкновение с астероидом #16.10.2024 (Прикрутил анимацию взрыва астероида при ударе. Астероид пропадает)
+- 8.3 Столкновение с астероидом - это ваншот (щит может задоджить) (Уже можно сделать, но пока что нету смысла)
+ 9. Добавть очки + #16.10.2024
+ 10. Добавить возможность ставить игру на паузу (На кнопку Q) #25.09.2024
+- 11.1 Добавить новое оружие (Лазер. Особенность - прошивает насквозь, но долго перезаряжается) 
- 11.2 Добавить новое оружие (Ракетомет. Особенность - сплеш урон)
+- 11.3 Добавить новое оружие (Плазмомет. Особенность - высокий урон) 
+- 12.1 Добавить магазин в меню (Покупка щита, пуль и ещё чего-нибудь за очки к новому раунду) (Кнопка есть, а магаза нету.)
- 12.2 Добавить щит и анимацию к нему, звуки 
- 12.3 Сделать пули не бесконечными 
+- 12.4 БОЛЬШЕ ОРУЖИЯ, УРААААДАААА 
+ 13.1 Добавить меню (Пока говёное, но есть) #16.10.2024 (Сделал нормальный интерфейс, переделал кнопки) #17.10.2024
+ 13.2 Несколько окон (возможность переключение) (В дальнейшем структурирую получше. #17.10.2024
                                                  Нужно будет сделать класс окна и контроллер, всё перенести туда, а не держать в MainWindow)
+ 13.3 Глав.меню
+ 13.4 Настройки
+- 13.5 Магазин (Кнопка и функция отрисовки окна есть, но невктивно всё ввиду отсутствия предметов для продажи, инвентаря и т.д.) 
+ 14.1 Разный саундтрек в игре и в меню #16.10.2024
+ 14.2 Разные обои в меню и в игре #17.10.2024
+ 15.1 Сделать врагов. (текстурки +, звуки -) #20.11.2024
+ 15.2 Сделать для врагов ИИ (Маневрируют/избегают астероиды/стреляют и уклоняются от пуль). #20.11.2024 
  (Поправил ботов, теперь они нормально работают. Только пару багов есть, но не критичных. Можно поправить позже.) #26.11.2024
- 16. Добавить в магазине Улучшения 
- 17.1 ДОБАВИТЬ ВОЗМОЖНОСТЬ СОХРАНЕНИЯ (Через json) 
- 17.2 Защитить файлики сохранения от изменения (Например, хеш. Или дубликат где-то в другом месте). 
- 18. Добавить игроку инвентарь (И сохранять это, в том же json). 
- 19. Разные модельки игрока, в зависимости от полученного урона. (текстурки +, в папке other) 
- 20. При нажатии на кнопку играть, добавить окно выбора снаряжения, купленного в магазине. 
      Мб переместить и сам магазин в это окно, считать его за часть игрового процесса
      (Под рогалик. Умер - закупился и дальше. Умер, закупился, умер, закупился...)
- 21.1 Добавить несколько уровней и боссов между ними.
- 21.2 Открытия меню магазина между уравнями.
  (Это заставит игрока рисковать, набирая очки для магазина)
- 22 Переработать игрока и противников, сделав общий класс ship

+ ОБЯЗАТЕЛЬНО, но потом: не забыть правильно обрезать текстуры, а то 1/3-1/2 текстуры - прозрачные пиксели, 
которые идут за часть обьекта. Брух.

+ Есть утечка ОЗУ. Немного, но куда - вопрос. 
Подозреваю, что группы не очищаются. (решено)
'''

from pygame import display, event, mixer, time, sprite, key
from pygame.locals import *
from random import choice, randint
from config import *
from time import time as t

from game import Game
from player import Player
from bullet import Bullet
from asteroid import Asteroid
from enemy import Enemy

class Main(Game):
    def __init__(self, game_name='CosmoBattle'):
        Game.__init__(self, game_name)  

        #self.bullet_group = []
        #self.asteroid_group = []

        self.bullet_group = sprite.Group()
        self.asteroid_group = sprite.Group()
        self.enemy_group = sprite.Group()
        self.enemy_bullet_group = sprite.Group()

        self.timer_spawn_stone = 450
        self.event_spawn_stone = USEREVENT + 1
        self.timer_spawn_enumy = 10000
        self.event_spawn_enemy = USEREVENT + 2
        time.set_timer(self.event_spawn_stone, self.timer_spawn_stone)
        time.set_timer(self.event_spawn_enemy, self.timer_spawn_enumy)

        self.max_count_enemy = 3

        #self.start_time_fire = t()
        self.start_time_inv = t()
        self.time_invulnerability = 1.5 # Время бессмертия
                                        # После получения урона

    def score(self):
        self.text_title(txt=self.GAME_POINT, pos=(W - 60, 100))

    '''
    def collize(self, obj1=None, obj2=None, group1=None, group2=None):
        if group1 is None and group2 is None:
            if obj1.rect.colliderect(obj2.rect):
                return True
            else:
                return False
            
        elif obj2 is None and group2 is None:
            for obj_g in group1:
                if obj1.rect.colliderect(obj_g.rect):
                    return True, obj_g
                else:
                    return False, obj_g
    '''

    # У меня болят глаза когда я смотрю на это, но мне лень делать по другому.
    # Мб когда-нибудь потом...
    def game_over(self):
        if self.player.xp <= 0:
            print('Игрок проиграл')

            self.reload_sound(MENUGAMESOUND)
            self.running = False

            self.asteroid_group.empty()
            self.bullet_group.empty()
            self.enemy_group.empty()
            self.enemy_bullet_group.empty()

            self.player.xp = 100
        else:
            self.draw_bar(HEALTHBAR, HEALTHDOT, self.player.xp, (W - 190, 20))
        
    def run(self):
        while self.play:
            display.update()
            self.clock.tick(FPS)
            events = event.get()
            keys = key.get_pressed() 

            # В игре или в меню
            if self.running: 
                self.draw_bg(self.bg_game, 2)
                #if self.collize(group1=self.bullet_group, group2=self.asteroid_group):

                collisions = sprite.groupcollide(self.bullet_group, self.asteroid_group, dokilla=True, dokillb=False, collided=sprite.collide_mask) #, dokillb=True
                # Cтолкновения между камушком и пулькой, ЫЫ
                for bullet, asteroids in collisions.items():
                    for asteroid in asteroids:
                        asteroid.xp -= bullet.damage

                        if asteroid.xp <= 0:
                            asteroid.start_anim_dead = True
                            asteroid.destruction_sound.play()
                        
                            self.GAME_POINT += 4

                collisions = sprite.groupcollide(self.bullet_group, self.enemy_group, dokilla=True, dokillb=False, collided=sprite.collide_mask) #, dokillb=True
                # Cтолкновения между противником и пулькой
                for bullet, enemys in collisions.items():
                    for enem in enemys:
                        enem.xp -= bullet.damage
                        print(f'Урона нанесено: {bullet.damage}')

                        if enem.xp <= 0:
                            enem.start_anim_dead = True
                            enem.destruction_sound.play()
                        
                            self.GAME_POINT += 10

                collisions = sprite.groupcollide(self.asteroid_group, self.enemy_group, dokilla=False, dokillb=False, collided=sprite.collide_mask) #, dokillb=True
                # Cтолкновения между противником и камушком
                for asteroid, enemys in collisions.items():
                    for enem in enemys:
                        enem.xp -= asteroid.damage
                        asteroid.start_anim_dead = True

                        if enem.xp <= 0:
                            enem.start_anim_dead = True
                            enem.destruction_sound.play()
                        
                            self.GAME_POINT += 1

                []
                collisions = sprite.spritecollide(self.player, self.enemy_bullet_group, True, collided=sprite.collide_mask) #, dokillb=True
                # Cтолкновения между игроком и пулькой противника
                if collisions and t() - self.start_time_inv >= self.time_invulnerability:
                    self.player.xp -= collisions[0].damage
                    self.start_time_inv = t()

                # Cтолкновения между игроком и камушком
                collisions = sprite.spritecollide(self.player, self.asteroid_group, False, collided=sprite.collide_mask)
                if collisions and t() - self.start_time_inv >= self.time_invulnerability:
                    self.player.xp -= collisions[0].damage

                    collisions[0].start_anim_dead = True
                    collisions[0].destruction_sound.play()
                        
                    self.start_time_inv = t()

                    for asteroid in collisions:
                        asteroid.start_anim_dead = True

                for game_event in events:
                    if game_event.type == KEYDOWN and self.running:
                        if game_event.key == K_q:
                            self.pause() 

                    if game_event.type == self.event_spawn_stone: # and not self.GAMEOVER
                        self.asteroid_group.add(Asteroid(80, 80, randint(2, 8), self.screen, ASTEROID, (randint(0, W-60), -60)))
                        self.timer_spawn_stone = randint(100, 1500)

                    if game_event.type == self.event_spawn_enemy and len(self.enemy_group) < self.max_count_enemy: # and not self.GAMEOVER
                        bot = Enemy(60, 60, 6, self.screen, ENEMY, (randint(60, W-60), -60))
                        bot.change_activ_gun(choice(['пушка', 'лазер', 'плазма']))
                        self.enemy_group.add(bot) # , follow_player_flag=choice([True, False])
                        #self.timer_spawn_enemy = randint(100, 1500)

                for game_event in keys:
                    #if game_event.type == KEYDOWN:
                    if keys[K_SPACE]:
                        bul = self.player.fire()
                        if bul:
                            self.bullet_group.add(bul)
                                #self.player.change_activ_gun('пушка')  
                    if keys[K_1]:
                        self.player.change_activ_gun('пушка')
                    if keys[K_2]:
                        self.player.change_activ_gun('плазма')
                    if keys[K_3]:
                        self.player.change_activ_gun('лазер')   

                self.bullet_group.update()
                self.bullet_group.draw(self.screen)   
                self.asteroid_group.update()
                self.asteroid_group.draw(self.screen)    
                self.enemy_bullet_group.update()
                self.enemy_bullet_group.draw(self.screen)
                
                self.game_over()
                self.score() 

                for enem in self.enemy_group:
                    enem.update(self.asteroid_group, self.bullet_group, self.enemy_bullet_group, self.enemy_group, self.player)
                    enem.anim_fire()
                
                #for enem in self.enemy_group:
                    
                self.enemy_group.draw(self.screen)

                self.player.anim_fire()
                self.player.draw()
                self.player.move()

            else:
                self.draw_bg(self.bg_menu, 1)
                self.window_manager()
                self.player = Player(60, 60, 7, self.screen, PLAYER, (W/2, H-100), xp=self.player_xp)
                self.player_xp = 100 + (10 * INVENTORY['improvements']['healf'])

                for eve in events:
                    self.handle_event(eve)

            for eve in events:
                if eve.type == QUIT:
                    self.play = False
                    quit()
                
if __name__ == '__main__':
    main = Main()
    main.run()