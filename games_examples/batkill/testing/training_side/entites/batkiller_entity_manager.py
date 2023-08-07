from games_examples.batkill.testing.training_side.entites.player_entity import PlayerEntity
from games_examples.batkill.testing.training_side.entites.bat_entity import BatEntity
from xumes.training_module import EntityManager


class BatKillerEntityManager(EntityManager):

    def build_entity(self, game_element_state):
        if game_element_state.type == "StandardPlayer":
            return PlayerEntity.build(game_element_state.state)
        if game_element_state.type == "Bat":
            return BatEntity.build(game_element_state.state)
