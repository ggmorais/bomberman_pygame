from src.game import Game


def main():
    game = Game()

    while game.is_running:
        game.update()
        game.render()

if __name__ == "__main__":
    main()
