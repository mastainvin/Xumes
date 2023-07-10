from abc import ABC

from src.xumes import GameElementState
from src.xumes import StateObservable
from games_examples.snake.src.fruit import Fruit
from games_examples.snake.src.snake import Snake


class FruitObservable(Fruit, StateObservable, ABC):

    def __init__(self, observers, name):
        StateObservable.__init__(self, observable_object=self, observers=observers, name=name)
        Fruit.__init__(self)
        self.notify()

    def randomize(self):
        super().randomize()
        self.notify()

    def state(self):
        return GameElementState({
            "x": self.x,
            "y": self.y
        })


class SnakeObservable(Snake, StateObservable, ABC):

    def __init__(self, observers, name):
        StateObservable.__init__(self, observable_object=self, observers=observers, name=name)
        Snake.__init__(self)
        self.notify()

    def move_snake(self):
        super().move_snake()
        self.notify()

    def state(self):
        return GameElementState({
            "body": [{"x": vector.x, "y": vector.y} for vector in self.body],
            "direction": {"x": self.direction.x, "y": self.direction.y}
        })
