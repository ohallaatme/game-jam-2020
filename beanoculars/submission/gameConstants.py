import os
from pathlib import Path

FULLSCREEN = False

# CONSTANTS
TILE_SIZE = 32  # x32 = 256px
PLAYER_SCALING = 1
TILE_SCALING = 1

WINDOW_WIDTH = 512 * 2
WINDOW_HEIGHT = 512
WINDOW_TITLE = 'Insane Irradiated Insects'

LEFT_FACING = 3
RIGHT_FACING = 2
DOWN_FACING = 1
UP_FACING = 0

# GAME MODES
GM_MENU = 0
GM_GAME = 1

# SPEED
MOVE_SPEED = 200
MOVE_SPEED_CHARGED = 0.8 * MOVE_SPEED

ENTITY_MS = 50

# ENTITY TYPES
E_ANT = 1
E_MOSQUITO = 2
E_SPIDER = 3
E_DUNG_BEETLE = 4

T_SPRAY = 10
T_LAMP = 11
T_VACUUM = 12

# ROWS
TOP_ROW = 0
MID_ROW = 1
BOT_ROW = 2

# VOLUME
VOLUME = 0.5

# UPDATE RATES FOR ENTITIES
UR_PLAYER = 1

UR_MOSQUITO = 10
UR_ANT = 10
UR_SPIDER = 10
UR_DUNG_BEETLE = 10

UR_SPRAY = 30
UR_LAMP = 30
UR_VACUUM = 30

# num of frames
F_ANT = 2
F_MOSQUITO = 2
F_SPIDER = 2
F_DUNG_BEETLE = 2

F_SPRAY = 2
F_LAMP = 2
F_VACUUM = 2

# BASE POSITIONS FOR TURRETS AND PLAYER
BP_PLAYER = [14, 7]
BP_SPRAY = [10, 12]
BP_LAMP = [15, 9]
BP_VACUUM = [11, 4]

# WAVES MANAGER
PREMADE_WAVES = 5

# TILES POSITIONS CHANGING DIRECTIONS
TILE_UP = [[12, 11], [16, 11], [29, 11], [7, 3], [8, 4], [15, 1], [16, 4]]
TILE_DOWN = [[4, 13], [6, 12], [13, 12], [20, 14], [22, 13], [24, 8], [12, 5], [20, 5], [21, 4]]
TILE_RIGHT = [[4, 12], [6, 11], [12, 12], [16, 14], [20, 13], [22, 11], [29, 12], [24, 7], [7, 4], [8, 5], [12, 1],
              [15, 4], [16, 5], [20, 4], [21, 3], [13, 11]]

PATH = {}
PATH['project'] = Path(os.path.dirname(__file__))
PATH['img'] = PATH['project'] / "images"
PATH['sound'] = PATH['project'] / "sounds"
PATH['maps'] = PATH['project'] / "tmx_maps"
