from src.xumes import IStateEntity


class SnakeEntity(IStateEntity):

    def __init__(self):
        self.body = []
        self.direction = None

    def update(self, state) -> None:
        self.body.clear()
        for c in state["body"]:
            vec = [c["x"], c["y"]]
            self.body.append(vec)
        self.direction = (state["direction"]["x"], state["direction"]["y"])

    @staticmethod
    def build(state):
        body = []
        for c in state["body"]:
            vec = [c["x"], c["y"]]
            body.append(vec)

        snake = SnakeEntity()
        snake.body = body
        snake.direction = (state["direction"]["x"], state["direction"]["y"])

        return snake
