import math
import pygame as pg
from src.bomb import Bomb
from src.state_manager import STATE


class Player:
    def __init__(self):
        self.sprite = pg.sprite.Sprite()
        self.sprite.image = pg.image.load("assets/Bomberman/Front/Bman_F_f00.png")
        self.rect = self.sprite.image.get_rect()

        self.speed = 5
        self.bombs_limit = 3
        self.bombs = []

        self.last_move = None

    def get_fake_rect(self):
        rc = self.rect.copy()
        rc.height = 32
        rc.width = 32

        rc.x = rc.x + (self.rect.w - rc.w) / 2
        rc.y = rc.y + self.rect.h - rc.h

        return rc

    def render(self, target: pg.Surface):
        target.blit(self.sprite.image, self.rect)

    def update(self):
        bombs_to_remove = []

        for i, (bomb_x, bomb_y) in enumerate(self.bombs):
            if not STATE.grid.get_tile(bomb_x, bomb_y, "bombs"):
                bombs_to_remove.append(i)

        self.bombs = [bomb for i, bomb in enumerate(self.bombs) if i not in bombs_to_remove]

        key_pressed = pg.key.get_pressed()

        if key_pressed[pg.K_d]:
            self.rect.move_ip(self.speed, 0)
            self.last_move = "right"
        elif key_pressed[pg.K_a]:
            self.rect.move_ip(-self.speed, 0)
            self.last_move = "left"
        elif key_pressed[pg.K_s]:
            self.rect.move_ip(0, self.speed)
            self.last_move = "down"
        elif key_pressed[pg.K_w]:
            self.rect.move_ip(0, -self.speed)
            self.last_move = "up"

        if key_pressed[pg.K_SPACE]:
            if len(self.bombs) < self.bombs_limit:
                x, y = STATE.grid.get_cell_world_pos(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2)
                x = math.floor(x)
                y = round(y)
                if (x, y) not in self.bombs:
                    STATE.grid.add_tile(x, y, "bombs", Bomb(x, y))

                    self.bombs.append((x, y))
