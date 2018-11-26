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
SCREENRECT = Rect(0, 0, 600, 650)

# Player Speed
PLAYER_SPEED = 12
PLAYER_SHOT_ODDS = 25

# Enemy
ENEMY_WIDTH = 28
ENEMY_HEIGHT = 26
ENEMY_ODDS = 48
MAX_ENEMIES = 300
ENEMY_SHOT_ODDS = 50
MAX_ENEMY_SHOT = 150

# Shots
MAX_SHOTS = 5
SHOT_SPEED = 10

# Level-based properties
TOTAL_LEVELS = 3
ENEMIES_PER_ROW = [0, 6, 6, 8]
ENEMY_ROWS = [0, 2, 3, 3]
TOTAL_ENEMIES = [0, 12, 30, 54]
ENEMY_SPEED = [0, 4, 5, 6]
ENEMY_DROP_DIST = [0, 10, 15, 20]
