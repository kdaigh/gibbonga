## @file constants.py
#  File containing game constants
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 10/18/18

from pygame.locals import *


# Frames Per Second
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game Font
GAME_FONT = "assets/fonts/arcadeclassic.ttf"
TEXT_SIZE = 25

# Game Menu
MESSAGE_SIZE = 50

# Window Size
#SCREENRECT = Rect(0, 0, 640, 480)
SCREENRECT = Rect(0, 0, 600, 650)

# Player Speed
PLAYER_SPEED = 12

# Enemy
ENEMY_SPEED = 4
ENEMY_DROP = 10
ENEMY_ODDS = 48
ENEMY_SIZE = (26, 24)
MAX_ENEMY_SHOT = 150
ENEMY_SHOT_ODDS = 50
MAX_ENEMIES = 300

# Shots
MAX_SHOTS = 5
SHOT_SPEED = 10

# Levels / Fleet expansion
ENEMIES_PER_ROW = 6
ENEMY_ROWS = 2
ENEMY_WIDTH = 28
ENEMY_HEIGHT = 26
