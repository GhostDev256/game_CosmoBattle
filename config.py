W = 1280 # Ширина
H = 760 # Высота

FPS = 40

GAMEPOINT = r''
HEART = r'content\img\heart\heart2.png'

PLAYER = r'content\img\player\P_Full_health.png'
ENEMYANIM = r'content\img\enemy'
ENEMY = r'content\img\enemy\tile000.png'

BG_GAME = r'content\img\bg\bg_game.jpg'
BG_MENU = r'content\img\bg\bg_menu.jpg'

GUNFIRESOUND = r'content\sound\shot'
BUL = r'content\img\bullets'
BASEBUL = r'content\img\bullets\tile000.png'
GUN = r'content\img\gun'
PLASMAGUN = r'content\img\plasma gun'
PLASMA = r'content\img\plasma'
BASEPLASMA = r'content\img\plasma\tile000.png'
LASERGUN = r'content\img\laser gun'
LASER = r'content\img\laser'
BASELASER = r'content\img\laser\tile000.png'

ASTEROIDANIM = r'content\img\asteroid'
ASTEROID = r'content\img\asteroid\tile000.png'

GAMESOUND = r'content\sound\game'
MENUGAMESOUND = r'content\sound\menu'
ASTEROIDDESTRUCTSOUND = r'content\sound\asteroid destruction\asteroid_destruction.wav'

HEALTHBAR = r'content\img\health bar\Health_Bar_Table.png'
HEALTHDOT = r'content\img\health bar\Health_Dot.png'

ARMORBAR = r'content\img\armor bar\Armor_Bar_Table.png'
ARMORDOT = r'content\img\armor bar\Armor_Dot.png'

WINDOW = r'content\img\window\Window.png'

PRESS_BUTTONSOUND = r'content\sound\button sound\press_sound.wav' # При наведении
CLICK_BUTTONSOUND = r'content\sound\button sound\click_sound.wav' # При нажатии

BASE_BUTTONICON = r'content\img\button\Button_Normal.png'
PRESS_BUTTONICON = r'content\img\button\Button_Hover.png'
CLICK_BUTTONICON = r'content\img\button\Button_Active.png'

SCROLLBAR = r'content\img\slider\ScrollBar.png'
KNOB = r'content\img\slider\Slider.png'

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

INVENTORY = {
            'weapon': 
                {
                    'пушка': True, 
                    'плазма': False, 
                    'лазер': False, 
                    'ракеты': False, 
                    'shield': False
                },
            'improvements': 
                {
                    'damage': 0,
                    'healf': 0,
                    'armor': 0,
                    'improvements_shield': 0
                }
            }

OBJECT_ID = {1: 'пушка', 2: 'плазма', 3: 'лазер',
             4: 'ракеты', 5: 'shield', 6: 'damage',
             7: 'healf', 8: 'armor', 9: 'improvements_shield',
             10: 'пусто', 11: 'пусто', 12: 'пусто',}