
from xumes.game_module.i_game_event import IGameEvent


def key_down(key):
    # Create and post event "keydown"
    import pygame
    event = pygame.event.Event(pygame.KEYDOWN, key=key)
    pygame.event.post(event)


def key_up(key):
    # Create and post event "keyup"
    import pygame
    event = pygame.event.Event(pygame.KEYUP, key=key)
    pygame.event.post(event)


class Up(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(key=pygame.K_UP)

    def release(self) -> None:
        import pygame
        key_up(key=pygame.K_DOWN)


# noinspection DuplicatedCode
class Down(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_DOWN)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_DOWN)


class Left(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_LEFT)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_LEFT)


class Right(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_RIGHT)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_RIGHT)


class Space(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_SPACE)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_SPACE)


class KeyA(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_a)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_a)


class KeyB(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_b)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_b)


class KeyC(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_c)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_c)


class KeyD(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_d)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_d)


class KeyE(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_e)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_e)


class KeyF(IGameEvent):
    def press(self) -> None:
        import pygame
        key_down(pygame.K_f)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_f)


class KeyG(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_g)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_g)


class KeyH(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_h)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_h)


class KeyI(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_i)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_i)


class KeyJ(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_j)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_j)


class KeyK(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_k)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_k)


class KeyL(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_l)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_l)


class KeyM(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_m)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_m)


class KeyN(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_n)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_n)


class KeyO(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_o)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_o)


class KeyP(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_p)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_p)


class KeyQ(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_q)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_q)


class KeyR(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_r)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_r)


class KeyS(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_s)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_s)


class KeyT(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_t)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_t)


class KeyU(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_u)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_u)


# noinspection DuplicatedCode
class KeyV(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_v)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_v)


class KeyW(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_w)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_w)


class KeyX(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_x)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_x)


class KeyY(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_y)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_y)


class KeyZ(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_z)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_z)


class Key0(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_0)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_0)


class Key1(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_1)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_1)


class Key2(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_2)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_2)


class Key3(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_3)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_3)


class Key4(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_4)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_4)


class Key5(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_5)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_5)


class Key6(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_6)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_6)


class Key7(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_7)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_7)


class Key8(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_8)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_8)


class Key9(IGameEvent):

    def press(self) -> None:
        import pygame
        key_down(pygame.K_9)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_9)


class Key0Pad(IGameEvent):
    def press(self) -> None:
        import pygame
        key_down(pygame.K_KP0)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_KP0)


class Key1Pad(IGameEvent):
    def press(self) -> None:
        import pygame
        key_down(pygame.K_KP1)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_KP1)


class Key2Pad(IGameEvent):
    def press(self) -> None:
        import pygame
        key_down(pygame.K_KP2)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_KP2)


class Key3Pad(IGameEvent):
    def press(self) -> None:
        import pygame
        key_down(pygame.K_KP3)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_KP3)


class Key4Pad(IGameEvent):
    def press(self) -> None:
        import pygame
        key_down(pygame.K_KP4)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_KP4)


class Key5Pad(IGameEvent):
    def press(self) -> None:
        import pygame
        key_down(pygame.K_KP5)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_KP5)


class Key6Pad(IGameEvent):
    def press(self) -> None:
        import pygame
        key_down(pygame.K_KP6)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_KP6)


class Key7Pad(IGameEvent):
    def press(self) -> None:
        import pygame
        key_down(pygame.K_KP7)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_KP7)


class Key8Pad(IGameEvent):
    def press(self) -> None:
        import pygame
        key_down(pygame.K_KP8)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_KP8)


class Key9Pad(IGameEvent):
    def press(self) -> None:
        import pygame
        key_down(pygame.K_KP9)

    def release(self) -> None:
        import pygame
        key_up(pygame.K_KP9)
