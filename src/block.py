import pygame as pg


class Block:
    def __init__(self, x: int, y: int, image_path: str):
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def render(self, target: pg.Surface):
        target.blit(self.image, self.rect)


class SolidBlock(Block):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "assets/Blocks/SolidBlock.png")


class ExplodableBlock(Block):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "assets/Blocks/ExplodableBlock.png")


class BackgroundBlock(Block):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "assets/Blocks/BackgroundTile.png")
