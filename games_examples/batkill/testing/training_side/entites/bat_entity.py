from xumes.training_module import IStateEntity


class BatEntity(IStateEntity):

    def __init__(self, position, direction, speed, dead, collider_rect):
        self.position = position
        self.direction = direction
        self.speed = speed
        self.dead = dead
        self.collider_rect = collider_rect

    def update(self, state):
        self.position = state["position"]["x"], state["position"]["y"]
        self.direction = state["direction"]
        self.speed = state["speed"]
        self.dead = state["dead"]
        self.collider_rect = state["collider_rect"]

    @staticmethod
    def build(state):
        bat = BatEntity((state["position"]["x"], state["position"]["y"]), state["direction"], state["speed"],
                        state["dead"], state["collider_rect"])
        return bat
