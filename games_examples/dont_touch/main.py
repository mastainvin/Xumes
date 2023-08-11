import pygame

from games_examples.dont_touch.src.components.game_status import GameStatus
from games_examples.dont_touch.src.config import Config
from games_examples.dont_touch.src.global_state import GlobalState

pygame.init()

FramePerSec = pygame.time.Clock()


def update_game_display():
    pygame.display.update()
    FramePerSec.tick(Config.FPS)


def main():
    while True:
        if GlobalState.GAME_STATE == GameStatus.MAIN_MENU:
            main_menu_phase()
        elif GlobalState.GAME_STATE == GameStatus.GAMEPLAY:
            gameplay_phase()
        elif GlobalState.GAME_STATE == GameStatus.GAME_END:
            exit_game_phase()

        update_game_display()


if __name__ == "__main__":
    main()
