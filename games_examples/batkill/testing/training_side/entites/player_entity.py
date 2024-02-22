from xumes.trainer import IStateEntity


class PlayerEntity(IStateEntity):

    def __init__(self, position, direction, jump, attack_state, attack_duration, cool_down_state,
                 cool_down_duration, attack_rect, facing_nearest_bat, lives, score):
        self.position = position
        self.direction = direction
        self.jump = jump
        self.attack_state = attack_state
        self.attack_duration = attack_duration
        self.cool_down_state = cool_down_state
        self.cool_down_duration = cool_down_duration
        self.attack_rect = attack_rect
        self.facing_nearest_bat = facing_nearest_bat
        self.lives = lives
        self.score = score

    def update(self, state):
        self.position = state["position"]["x"], state["position"]["y"]
        self.direction = state["direction"]
        self.jump = state["jump"]
        self.attack_state = state["attack_state"]
        self.attack_duration = state["attack_duration"]
        self.cool_down_state = state["cool_down_state"]
        self.cool_down_duration = state["cool_down_duration"]
        self.attack_rect = state["attack_rect"]
        self.facing_nearest_bat = state["facing_nearest_bat"]
        self.lives = state["lives"]
        self.score = state["score"]

    @staticmethod
    def build(state):
        player = PlayerEntity((state["position"]["x"], state["position"]["y"]), state["direction"], state["jump"],
                              state["attack_state"], state["attack_duration"], state["cool_down_state"],
                              state["cool_down_duration"], state["attack_rect"], state["facing_nearest_bat"],
                              state["lives"], state["score"])
        return player
