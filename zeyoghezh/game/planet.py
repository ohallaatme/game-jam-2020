import arcade
import logging
from config import SCREEN_SIZE_Y, SCREEN_SIZE_X

logger = logging.getLogger()

BASE_SPEED = 1
PLANET_BASE_SPEED = 5 * BASE_SPEED
PUSH_BASE_SPEED = 2 * BASE_SPEED
PUSH_MAX_DISTANCE = 200  # The most a planet can be away from Yogh to be pushed
BASE_DAMAGE = 1e-4
PLANET_DAMAGE = {
    "ze": 20,
    "yogh": 5,
    "ezh": 7
}
MAX_ATTACK_DISTANCE = {
    "ze": 100,
    "yogh": 300,
    "ezh": 300
}
ATTACK_COLORS = {
    "ze": arcade.color.SILVER,
    "yogh": arcade.color.GOLD,
    "ezh": arcade.color.BRONZE
}
PLANET_SPRITES = {
    "ze": ":resources:images/items/coinSilver.png",
    "yogh": ":resources:images/items/coinGold.png",
    "ezh": ":resources:images/items/coinBronze.png"
}


class Planet(arcade.Sprite):
    def __init__(self, planet_name, *args, **kwargs):
        super().__init__(PLANET_SPRITES[planet_name], *args, **kwargs)
        self.name = planet_name
        self.speed_x = None
        self.speed_y = None
        self.health = 1
        self.can_push_planets = self.name == "yogh"
        self.can_blast_planets = self.name == "yogh"
        self.can_melee_planets = self.name == "ze"
        self.can_range_planets = self.name == "ezh"
        self.max_attack_distance = MAX_ATTACK_DISTANCE[self.name]
        self.base_damage = BASE_DAMAGE * PLANET_DAMAGE[self.name]
        self.attack_color = ATTACK_COLORS[self.name]

        self.parent = None
        self.others = None
        self.damage_on_others = None

        self.attacked_last_round = []

    def setup(
            self, parent, others, center_x, center_y,
            start_speed_x, start_speed_y):
        self.parent = parent
        self.others = others
        self.damage_on_others = {other.name: 0 for other in others}
        self.center_x = center_x
        self.center_y = center_y
        self.speed_x = start_speed_x
        self.speed_y = start_speed_y

    def move(self, delta_x=None, delta_y=None):
        if self.center_y > SCREEN_SIZE_Y - 5:
            self.speed_y = -abs(self.speed_y)
        if self.center_y < 0 + 5:
            self.speed_y = abs(self.speed_y)
        if self.center_x > SCREEN_SIZE_X - 5:
            self.speed_x = -abs(self.speed_x)
        if self.center_x < 0 + 5:
            self.speed_x = abs(self.speed_x)

        if delta_x is None:
            delta_x = self.speed_x * PLANET_BASE_SPEED
        if delta_y is None:
            delta_y = self.speed_y * PLANET_BASE_SPEED

        logger.debug(f"Moving {self.name}. {delta_x=}, {delta_y=}.")
        self.center_y += delta_y
        self.center_x += delta_x

    def try_push_others(self):
        if not self.can_push_planets:
            return
        for other in self.others:
            distance = arcade.get_distance_between_sprites(self, other)
            if distance < PUSH_MAX_DISTANCE:
                self.push_other(other)

    def push_other(self, other):
        # TODO improve this logic
        x_distance = other.center_x - self.center_x
        y_distance = other.center_y - self.center_y
        distance_sum = abs(x_distance) + abs(y_distance)
        x_distance_normalized = x_distance / distance_sum
        y_distance_normalized = y_distance / distance_sum
        x_push = x_distance_normalized * PUSH_BASE_SPEED
        y_push = y_distance_normalized * PUSH_BASE_SPEED
        logger.debug(
            f"{self.name} pushing {other.name}  ({x_distance=}, {y_distance=} "
            f"by {x_push=}, {y_push=}")

        if self.center_x > other.center_x:
            assert x_push < 0
        if self.center_x < other.center_x:
            assert x_push > 0
        if self.center_x == other.center_x:
            assert x_push == 0
        if self.center_y > other.center_y:
            assert y_push < 0
        if self.center_y < other.center_y:
            assert y_push > 0
        if self.center_y == other.center_y:
            assert y_push == 0
        if abs(x_distance) > abs(y_distance):
            assert abs(x_distance_normalized) > abs(y_distance_normalized)

        other.move(delta_x=x_push, delta_y=y_push)

    def try_attack_others(self):
        for other in self.others:
            distance = arcade.get_distance_between_sprites(self, other)
            if distance < self.max_attack_distance:
                self.attack_other(other)

    def attack_other(self, other):
        self.attacked_last_round.append(other)
        distance_between = arcade.get_distance_between_sprites(self, other)
        logger.debug(
            f"{self.name} attacking {other.name} "
            f"({distance_between=} for {self.base_damage}")
        # TODO improve this
        other.health -= self.base_damage
        self.damage_on_others[other.name] += self.base_damage
        other.scale = other.health
        if other.health < 0:
            other.die()

    def die(self):
        self.parent.game_over(f"{self.name} has died")

    def get_stats_str(self):
        total_damage_on_others = round(sum(self.damage_on_others.values()), 4)
        damage_on_others = {
            other: round(self.damage_on_others[other], 4)
            for other in self.damage_on_others}
        return f"{self.name}:\t{total_damage_on_others=}, {damage_on_others=}"
