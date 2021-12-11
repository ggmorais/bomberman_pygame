import pygame as pg
from src.constants import FPS, WINDOW_SIZE
from src.state_manager import STATE
from src.colors import Colors
from src.player import Player
from src.grid import Grid


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Bomberman")

        self.clock = pg.time.Clock()
        self.is_running = True
        self.window = pg.display.set_mode(WINDOW_SIZE)
        self.player = Player()

    def poll_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

    def check_collisions(self):
        if self.player.get_fake_rect().collidelist([tile.obj.rect for tile in STATE.grid.get_tiles("structures")]) > -1:
            last_move = self.player.last_move
        
            if last_move == "right":
                self.player.rect.move_ip(-self.player.speed, 0)
            elif last_move == "left" :
                self.player.rect.move_ip(self.player.speed, 0)
            elif last_move == "down" :
                self.player.rect.move_ip(0, -self.player.speed)
            elif last_move == "up" :
                self.player.rect.move_ip(0, self.player.speed)

    def render(self):
        self.window.fill(Colors.BLACK)

        STATE.grid.render(self.window)
        self.player.render(self.window)

        # pg.draw.rect(self.window, Colors.RED, self.player.get_fake_rect())

        pg.display.flip()

        self.clock.tick(FPS)

    def update(self):
        self.poll_events()

        STATE.grid.update()
        self.player.update()

        self.check_collisions()
