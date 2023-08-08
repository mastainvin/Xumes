from src.xumes import EntityManager
from src.xumes import GameElementState
from src.xumes import IStateEntity
from games_examples.snake.testing.test_training_service.entities.fruit_entity import FruitEntity
from games_examples.snake.testing.test_training_service.entities.snake_entity import SnakeEntity


class SnakeEntityManager(EntityManager):

    def build_entity(self, game_element_state: GameElementState) -> IStateEntity:
        if game_element_state.type == "Snake":
            return SnakeEntity.build(game_element_state.state)
        if game_element_state.type == "Fruit":
            return FruitEntity.build(game_element_state.state)
