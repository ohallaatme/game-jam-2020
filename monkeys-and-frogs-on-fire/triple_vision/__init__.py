from enum import IntEnum


class Settings:
    TITLE = 'Triple Vision'
    WINDOW_SIZE = (1280, 720)
    SCALING = 3
    MAP_SIZE = (50, 50)
    ON_CARD_HOVER_SLOWDOWN_MULTIPLIER = 50


class Tile:
    SIZE = 16
    SCALED = SIZE * Settings.SCALING


class SoundSettings:
    FADE_FREQUENCY = 0.1
    FADE_AMOUNT = 0.05


class Direction(IntEnum):
    LEFT: int = 1
    RIGHT: int = 0
