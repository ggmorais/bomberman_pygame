import random
import pygame as pg
from src.globals import WINDOW_SIZE
from src.block import Block, SolidBlock, ExplodableBlock, BackgroundBlock
from dataclasses import dataclass


@dataclass
class Tile:
    x: int
    y: int
    obj: Block
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

    def get_tiles(self, layer: str):
        return [tile for tile in self.tiles if tile.layer == layer]

    def get_tile(self, x: int, y: int, layer: str):
        for tile in self.tiles:
            if tile.x == x and tile.y == y and tile.layer == layer:
                return tile

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
