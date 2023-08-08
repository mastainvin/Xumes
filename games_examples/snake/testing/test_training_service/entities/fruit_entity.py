
from src.xumes import IStateEntity


class FruitEntity(IStateEntity):

    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, state) -> None:
        self.x = state["x"]
        self.y = state["y"]

    @staticmethod
    def build(state):
        fruit = FruitEntity()
        fruit.x = state["x"]
        fruit.y = state["y"]
        return fruit
