import random
import pygame as pg
from src.constants import WINDOW_SIZE
from src.block import Block, SolidBlock, ExplodableBlock, BackgroundBlock
from dataclasses import dataclass
from typing import Any


@dataclass
class Tile:
    x: int
    y: int
    obj: Any
    layer: str


class Grid:
    def __init__(self, x: int, y: int, cell_size: int):
        self.x = x
        self.y = y
        self.size = cell_size

        self.tiles: list[Tile] = []

        self.spawn_background()
        self.spawn_solids()
        self.spawn_explodables()

    def remove_tile(self, x: int, y: int, layer: str):
        self.tiles = [
            tile
            for tile in self.tiles
            if tile.x != x and tile.y != y and tile.layer != layer
        ]

    def remove_tile_by_obj(self, obj: Any):
        self.tiles = [tile for tile in self.tiles if tile.obj != obj]

    def add_tile(self, x: int, y: int, layer: str, obj: Any):
        obj_size = obj.rect.width
        obj.rect.x = x * self.size + (self.size - obj_size) / 2
        obj.rect.y = y * self.size + (self.size - obj_size) / 2

        self.tiles.append(Tile(x, y, obj, layer))

    def get_tiles(self, layer: str):
        return [tile for tile in self.tiles if tile.layer == layer]

    def get_tile(self, x: int, y: int, layer: str):
        for tile in self.tiles:
            if tile.x == x and tile.y == y and tile.layer == layer:
                return tile

    def get_cell_world_pos(self, x: int, y: int):
        return (x / self.size, y / self.size)

    def get_world_cell_pos(self, x: int, y: int):
        return (x * self.size, y * self.size)

    def spawn_background(self):
        for i in range(self.x):
            for j in range(self.y):
                self.tiles.append(Tile(
                    i, 
                    j, 
                    BackgroundBlock(i * self.size, j * self.size),
                    layer="background"
                ))

    def spawn_solids(self):
        for i in range(1, self.x, 2):
            for j in range(1, self.y, 2):
                self.tiles.append(Tile(
                    i, 
                    j, 
                    SolidBlock(i * self.size, j * self.size),
                    layer="structures"
                ))
        
    def spawn_explodables(self):
        for i in range(1, self.x - 1):
            for j in range(1, self.y - 1):
                if self.get_tile(i, j, "structures") is not None:
                    continue
                
                if random.randint(0, 2) == 1:
                    self.tiles.append(Tile(
                        i, 
                        j, 
                        ExplodableBlock(i * self.size, j * self.size),
                        layer="structures"
                    ))

    def render(self, target: pg.Surface):
        for tile in self.tiles:
            tile.obj.render(target)

    def update(self):
        for tile in self.tiles:
            if hasattr(tile.obj, "update"):
                tile.obj.update()
