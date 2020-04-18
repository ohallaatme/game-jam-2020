"""
Tricky Tricepticat
Domicidal
Python Discord | Game Jam 2020
"""
import os
from pathlib import Path

import arcade


UPDATES_PER_FRAME = 3

MOVEMENT_SPEED = 300

SPRITE_SCALING = 3

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Game Jam 2020"

# File paths for project and resources
path = {}
path['project'] = Path(os.path.dirname(__file__))
path['resources'] = path['project'] / "resources"
path['img'] = path['resources'] / "img"
path['sound'] = path['resources'] / "sound"


def load_texture_pair(filename):
    '''
    Load a texture pair, with the second being a mirror image.
    '''
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]


class Pirate(arcade.Sprite):
    '''
    Player class
    '''
    def __init__(self, sprite_root):
        super().__init__()
        self.name = sprite_root

        sprite_path = path['img'] / sprite_root
        self.texture_dict = {}
        self.texture_dict['run'] = [
            load_texture_pair(sprite_path / "run" / f"{i}.png")
            for i in range(1, len(os.listdir(sprite_path / "run"))+1)
        ]
        self.texture_dict['idle'] = [
            load_texture_pair(sprite_path / "idle" / f"{i}.png")
            for i in range(1, len(os.listdir(sprite_path / "idle"))+1)
        ]
        self.texture_dict['attack'] = [
            load_texture_pair(sprite_path / "attack" / f"{i}.png")
            for i in range(1, len(os.listdir(sprite_path / "attack"))+1)
        ]

        self.texture = self.texture_dict['idle'][0][0]
        self.bottom = 0

        self.cur_run_texture = 0
        self.cur_idle_texture = 0
        self.cur_attack_texture = 0

        self.character_face_direction = RIGHT_FACING

        self.is_idle = False

    def update_animation(self):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING

        elif (
                self.change_x > 0 and
                self.character_face_direction == LEFT_FACING
             ):
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.is_idle:
            frames = self.cur_idle_texture // UPDATES_PER_FRAME

            if frames == len(self.texture_dict['idle'])-1:
                self.cur_idle_texture = 0

            print(self.name, frames)
            self.texture = self.texture_dict['idle'][frames][
                self.character_face_direction
                ]

            self.cur_idle_texture += 1
            return

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.texture_dict['idle'][0][
                self.character_face_direction
                ]
            self.cur_run_texture, self.cur_idle_texture = 0, 0
            return

        # Walking animation

        frames = self.cur_run_texture // UPDATES_PER_FRAME

        if frames == len(self.texture_dict['run'])-1:
            self.cur_run_texture = 0

        print(self.name, frames)
        self.texture = self.texture_dict['run'][frames][
            self.character_face_direction
            ]

        self.cur_run_texture += 1

    def on_update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

        self.update_animation()


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)

        self.player_sprites = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        # Create your sprites and sprite lists here
        self.player_sprites = arcade.SpriteList()
        for i in ('captain', 'brawn', 'bald'):
            self.player_sprites.append(Pirate(i))
        self.player_sprites[0].center_x = 400
        self.player_sprites[1].center_x = 600
        self.player_sprites[2].center_x = 800

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame
        arcade.start_render()

        self.player_sprites.draw()

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        for sprite in self.player_sprites:
            # Calculate speed based on the keys pressed
            sprite.change_x = 0
            sprite.change_y = 0

            if self.up_pressed and not self.down_pressed:
                sprite.change_y = MOVEMENT_SPEED
            elif self.down_pressed and not self.up_pressed:
                sprite.change_y = -MOVEMENT_SPEED
            if self.left_pressed and not self.right_pressed:
                sprite.change_x = -MOVEMENT_SPEED
            elif self.right_pressed and not self.left_pressed:
                sprite.change_x = MOVEMENT_SPEED

        # Call update to move the sprite
        # If using a physics engine, call update on it instead of the sprite
        # list.
        self.player_sprites.on_update(delta_time)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
