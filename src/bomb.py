import pygame as pg
from src.state_manager import STATE
from src.block import ExplodableBlock, SolidBlock


class Bomb:
    def __init__(self, x: int = 0, y: int = 0, fire_distance: int = 3):
        self.image = pg.image.load("assets/Bomb/Bomb_f01.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fire_distance = fire_distance
        self.max_seconds = 3
        self.timer = pg.time.get_ticks()

    def explode(self):
        x, y = STATE.grid.get_cell_world_pos(self.rect.x, self.rect.y)
        x = round(x)
        y = round(y)

        def iter_and_explode_tiles(value, axis, add):
            for i in range(value + add, value + self.fire_distance + add):
                if axis == "x":
                    params = (i, y)
                elif axis == "y":
                    params = (x, i)

                tile = STATE.grid.get_tile(params[0], params[1], "structures")

                if tile and isinstance(tile.obj, SolidBlock):
                    break
                elif tile and isinstance(tile.obj, ExplodableBlock):
                    STATE.grid.remove_tile_by_obj(tile.obj)
                
                bomb_tile = STATE.grid.get_tile(params[0], params[1], "bombs")

                if bomb_tile and bomb_tile.obj != self:
                    bomb_tile.obj.explode()

        iter_and_explode_tiles(x, "x", 1)
        iter_and_explode_tiles(x, "x", -1)
        iter_and_explode_tiles(y, "y", 1)
        iter_and_explode_tiles(y, "y", -1)

        STATE.grid.remove_tile_by_obj(self)

    def render(self, target: pg.Surface):
        target.blit(self.image, self.rect)

    def update(self):
        elapsed_time = (pg.time.get_ticks() - self.timer) / 1000
        if elapsed_time >= self.max_seconds:
            self.explode()

        self.timer -= 1
