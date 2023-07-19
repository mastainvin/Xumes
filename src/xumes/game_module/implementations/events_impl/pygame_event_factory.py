from xumes.game_module.i_game_event import IGameEvent
from xumes.game_module.i_event_factory import EventFactory
from xumes.game_module.implementations.events_impl.pygame_events import Up, Down, Left, Right, Space, KeyA, KeyB, KeyC, \
    KeyD, KeyE, KeyF, KeyG, KeyH, KeyI, KeyJ, KeyK, KeyL, KeyM, KeyN, KeyO, KeyP, KeyQ, KeyR, KeyS, KeyT, KeyU, KeyV, \
    KeyW, KeyX, KeyY, KeyZ, Key0, Key1, Key2, Key3, Key4, Key5, Key6, Key7, Key8, Key9, Key1Pad, Key2Pad, Key3Pad, \
    Key4Pad, Key5Pad, Key6Pad, Key7Pad, Key8Pad, Key9Pad, Key0Pad


class PygameEventFactory(EventFactory):

    def clear(self):
        import pygame
        pygame.event.clear()

    def up(self) -> IGameEvent:
        return Up()

    def down(self) -> IGameEvent:
        return Down()

    def left(self) -> IGameEvent:
        return Left()

    def right(self) -> IGameEvent:
        return Right()

    def space(self) -> IGameEvent:
        return Space()

    def k_a(self) -> IGameEvent:
        return KeyA()

    def k_b(self) -> IGameEvent:
        return KeyB()

    def k_c(self) -> IGameEvent:
        return KeyC()

    def k_d(self) -> IGameEvent:
        return KeyD()

    def k_e(self) -> IGameEvent:
        return KeyE()

    def k_f(self) -> IGameEvent:
        return KeyF()

    def k_g(self) -> IGameEvent:
        return KeyG()

    def k_h(self) -> IGameEvent:
        return KeyH()

    def k_i(self) -> IGameEvent:
        return KeyI()

    def k_j(self) -> IGameEvent:
        return KeyJ()

    def k_k(self) -> IGameEvent:
        return KeyK()

    def k_l(self) -> IGameEvent:
        return KeyL()

    def k_m(self) -> IGameEvent:
        return KeyM()

    def k_n(self) -> IGameEvent:
        return KeyN()

    def k_o(self) -> IGameEvent:
        return KeyO()

    def k_p(self) -> IGameEvent:
        return KeyP()

    def k_q(self) -> IGameEvent:
        return KeyQ()

    def k_r(self) -> IGameEvent:
        return KeyR()

    def k_s(self) -> IGameEvent:
        return KeyS()

    def k_t(self) -> IGameEvent:
        return KeyT()

    def k_u(self) -> IGameEvent:
        return KeyU()

    def k_v(self) -> IGameEvent:
        return KeyV()

    def k_w(self) -> IGameEvent:
        return KeyW()

    def k_x(self) -> IGameEvent:
        return KeyX()

    def k_y(self) -> IGameEvent:
        return KeyY()

    def k_z(self) -> IGameEvent:
        return KeyZ()

    def k_0(self) -> IGameEvent:
        return Key0()

    def k_1(self) -> IGameEvent:
        return Key1()

    def k_2(self) -> IGameEvent:
        return Key2()

    def k_3(self) -> IGameEvent:
        return Key3()

    def k_4(self) -> IGameEvent:
        return Key4()

    def k_5(self) -> IGameEvent:
        return Key5()

    def k_6(self) -> IGameEvent:
        return Key6()

    def k_7(self) -> IGameEvent:
        return Key7()

    def k_8(self) -> IGameEvent:
        return Key8()

    def k_9(self) -> IGameEvent:
        return Key9()

    def k_1_pad(self) -> IGameEvent:
        return Key1Pad()

    def k_2_pad(self) -> IGameEvent:
        return Key2Pad()

    def k_3_pad(self) -> IGameEvent:
        return Key3Pad()

    def k_4_pad(self) -> IGameEvent:
        return Key4Pad()

    def k_5_pad(self) -> IGameEvent:
        return Key5Pad()

    def k_6_pad(self) -> IGameEvent:
        return Key6Pad()

    def k_7_pad(self) -> IGameEvent:
        return Key7Pad()

    def k_8_pad(self) -> IGameEvent:
        return Key8Pad()

    def k_9_pad(self) -> IGameEvent:
        return Key9Pad()

    def k_0_pad(self) -> IGameEvent:
        return Key0Pad()
