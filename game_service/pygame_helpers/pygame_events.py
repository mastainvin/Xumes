import pygame

from game_service.client_event import IClientEvent


def key_down(key: pygame.constants):
    event = pygame.event.Event(pygame.KEYDOWN, key=key)
    pygame.event.post(event)


def key_up(key: pygame.constants):
    event = pygame.event.Event(pygame.KEYUP, key=key)
    pygame.event.post(event)


class Up(IClientEvent):

    def press(self) -> None:
        key_down(key=pygame.K_UP)

    def release(self) -> None:
        key_up(key=pygame.K_DOWN)


class Down(IClientEvent):

    def press(self) -> None:
        key_down(pygame.K_DOWN)

    def release(self) -> None:
        key_up(pygame.K_DOWN)


class Left(IClientEvent):

    def press(self) -> None:
        key_down(pygame.K_LEFT)

    def release(self) -> None:
        key_up(pygame.K_LEFT)


class Right(IClientEvent):

    def press(self) -> None:
        key_down(pygame.K_RIGHT)

    def release(self) -> None:
        key_up(pygame.K_RIGHT)
