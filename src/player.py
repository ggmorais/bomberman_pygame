import pygame as pg


class Player:
    def __init__(self):
        self.sprite = pg.sprite.Sprite()
        self.sprite.image = pg.image.load("assets/Bomberman/Front/Bman_F_f00.png")
        self.rect = self.sprite.image.get_rect()

        self.speed = 5

        self.last_move = None

    def get_fake_rect(self):
        rc = self.rect.copy()
        rc.height = 48
        rc.width = 48

        rc.y = rc.y + rc.height * 1.5
        rc.x = rc.x + rc.width / 5

        return rc

    def render(self, target: pg.Surface):
        target.blit(self.sprite.image, self.rect)

    def update(self):
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
            
