from abc import ABC
from typing import final

from xumes.game_module.i_game_event import IGameEvent


class EventFactory(ABC):
    """
      The `EventFactory` abstract class provides methods for managing and creating game events.

      Methods:
          clear: Remove every event from the event queue.
          find_input: Build and return a GameEvent from an input string.
          nothing: Return a "nothing" game event that does not perform any action.
          up: Create and return a game event for the "up" action.
          down: Create and return a game event for the "down" action.
          left: Create and return a game event for the "left" action.
          right: Create and return a game event for the "right" action.
          space: Create and return a game event for the "space" action.
    """

    def __init__(self):
        self.actions = {
            "up": self.up,
            "down": self.down,
            "left": self.left,
            "right": self.right,
            "space": self.space,
            "nothing": self.nothing,
            "k_a": self.k_a,
            "k_b": self.k_b,
            "k_c": self.k_c,
            "k_d": self.k_d,
            "k_e": self.k_e,
            "k_f": self.k_f,
            "k_g": self.k_g,
            "k_h": self.k_h,
            "k_i": self.k_i,
            "k_j": self.k_j,
            "k_k": self.k_k,
            "k_l": self.k_l,
            "k_m": self.k_m,
            "k_n": self.k_n,
            "k_o": self.k_o,
            "k_p": self.k_p,
            "k_q": self.k_q,
            "k_r": self.k_r,
            "k_s": self.k_s,
            "k_t": self.k_t,
            "k_u": self.k_u,
            "k_v": self.k_v,
            "k_w": self.k_w,
            "k_x": self.k_x,
            "k_y": self.k_y,
            "k_z": self.k_z,
            "k_0": self.k_0,
            "k_1": self.k_1,
            "k_2": self.k_2,
            "k_3": self.k_3,
            "k_4": self.k_4,
            "k_5": self.k_5,
            "k_6": self.k_6,
            "k_7": self.k_7,
            "k_8": self.k_8,
            "k_9": self.k_9,
            "k_0_pad": self.k_0_pad,
            "k_1_pad": self.k_1_pad,
            "k_2_pad": self.k_2_pad,
            "k_3_pad": self.k_3_pad,
            "k_4_pad": self.k_4_pad,
            "k_5_pad": self.k_5_pad,
            "k_6_pad": self.k_6_pad,
            "k_7_pad": self.k_7_pad,
            "k_8_pad": self.k_8_pad,
            "k_9_pad": self.k_9_pad
        }

    def clear(self) -> None:
        """
        Remove every event from the event queue.
        """
        raise NotImplementedError

    @final
    def find_input(self, input_str: str) -> IGameEvent:
        """
        Build and return a GameEvent from an input string.
        :param input_str: representation of an action.
        :return: Corresponding GameEvent
        """
        return self.actions.get(input_str, self.nothing)()

    # noinspection PyMethodMayBeStatic
    def nothing(self) -> IGameEvent:
        """
        :return: A nothing game event, (not doing anything on the game).
        """
        class Nothing(IGameEvent):
            def press(self) -> None:
                pass

            def release(self) -> None:
                pass

        return Nothing()

    def up(self) -> IGameEvent:
        raise NotImplementedError

    def down(self) -> IGameEvent:
        raise NotImplementedError

    def left(self) -> IGameEvent:
        raise NotImplementedError

    def right(self) -> IGameEvent:
        raise NotImplementedError

    def space(self) -> IGameEvent:
        raise NotImplementedError

    def k_a(self) -> IGameEvent:
        raise NotImplementedError

    def k_b(self) -> IGameEvent:
        raise NotImplementedError

    def k_c(self) -> IGameEvent:
        raise NotImplementedError

    def k_d(self) -> IGameEvent:
        raise NotImplementedError

    def k_e(self) -> IGameEvent:
        raise NotImplementedError

    def k_f(self) -> IGameEvent:
        raise NotImplementedError

    def k_g(self) -> IGameEvent:
        raise NotImplementedError

    def k_h(self) -> IGameEvent:
        raise NotImplementedError

    def k_i(self) -> IGameEvent:
        raise NotImplementedError

    def k_j(self) -> IGameEvent:
        raise NotImplementedError

    def k_k(self) -> IGameEvent:
        raise NotImplementedError

    def k_l(self) -> IGameEvent:
        raise NotImplementedError

    def k_m(self) -> IGameEvent:
        raise NotImplementedError

    def k_n(self) -> IGameEvent:
        raise NotImplementedError

    def k_o(self) -> IGameEvent:
        raise NotImplementedError

    def k_p(self) -> IGameEvent:
        raise NotImplementedError

    def k_q(self) -> IGameEvent:
        raise NotImplementedError

    def k_r(self) -> IGameEvent:
        raise NotImplementedError

    def k_s(self) -> IGameEvent:
        raise NotImplementedError

    def k_t(self) -> IGameEvent:
        raise NotImplementedError

    def k_u(self) -> IGameEvent:
        raise NotImplementedError

    def k_v(self) -> IGameEvent:
        raise NotImplementedError

    def k_w(self) -> IGameEvent:
        raise NotImplementedError

    def k_x(self) -> IGameEvent:
        raise NotImplementedError

    def k_y(self) -> IGameEvent:
        raise NotImplementedError

    def k_z(self) -> IGameEvent:
        raise NotImplementedError

    def k_0(self) -> IGameEvent:
        raise NotImplementedError

    def k_1(self) -> IGameEvent:
        raise NotImplementedError

    def k_2(self) -> IGameEvent:
        raise NotImplementedError

    def k_3(self) -> IGameEvent:
        raise NotImplementedError

    def k_4(self) -> IGameEvent:
        raise NotImplementedError

    def k_5(self) -> IGameEvent:
        raise NotImplementedError

    def k_6(self) -> IGameEvent:
        raise NotImplementedError

    def k_7(self) -> IGameEvent:
        raise NotImplementedError

    def k_8(self) -> IGameEvent:
        raise NotImplementedError

    def k_9(self) -> IGameEvent:
        raise NotImplementedError

    def k_0_pad(self) -> IGameEvent:
        raise NotImplementedError

    def k_1_pad(self) -> IGameEvent:
        raise NotImplementedError

    def k_2_pad(self) -> IGameEvent:
        raise NotImplementedError

    def k_3_pad(self) -> IGameEvent:
        raise NotImplementedError

    def k_4_pad(self) -> IGameEvent:
        raise NotImplementedError

    def k_5_pad(self) -> IGameEvent:
        raise NotImplementedError

    def k_6_pad(self) -> IGameEvent:
        raise NotImplementedError

    def k_7_pad(self) -> IGameEvent:
        raise NotImplementedError

    def k_8_pad(self) -> IGameEvent:
        raise NotImplementedError

    def k_9_pad(self) -> IGameEvent:
        raise NotImplementedError

