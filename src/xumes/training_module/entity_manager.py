from abc import abstractmethod
from typing import Dict, final

from xumes.training_module.i_state_entity import IStateEntity
from xumes.training_module.game_element_state import GameElementState
from xumes.training_module.i_game_element_state_converter import IGameElementStateConverter


class EntityManager(IStateEntity):
    """
       The `EntityManager` class is responsible for managing game entities and updating the game state.

       Attributes:
           _game_element_state_converter: An object implementing the `IGameElementStateConverter` interface for converting game elements to states.
           _entities: A dictionary mapping entity names to their corresponding `IStateEntity` instances.
           _game_state: The current game state.

       Methods:
           update(state): Updates the game state when received.
           game_state: Property representing the current game state.
           get_all(): Retrieves all game observable entities.
           get(name): Retrieves an entity by its name.
           _update(game_element_state): Updates an existing game entity with the provided `game_element_state`.
           _add(game_element_state): Adds a new game entity with the provided `game_element_state`.
           convert(state_wrapper): Converts a game element, updates or adds it to the state.
           build_entity(game_element_state): Builds a game entity based on the provided `game_element_state`.
    """

    def __init__(self,
                 game_element_state_converter: IGameElementStateConverter
                 ):
        self._game_element_state_converter = game_element_state_converter
        self._entities: Dict[str, IStateEntity] = {
            "test_runner": self
        }
        self._game_state: str = ""

    def update_state(self, state) -> None:
        """
        Update the game state when receive it.
        :param state: game state (ex: "alive", "dead").
        """
        self._game_state = state["state"]

    @property
    @final
    def game_state(self):
        return self._game_state

    @final
    def get_all(self):
        """
        Get every game observables entities.
        :return: every entity
        """
        return self._entities

    @final
    def get(self, name: str):
        return self._entities[name]

    @final
    def _update(self, game_element_state: GameElementState):
        u = self.get(game_element_state.name).update_state(game_element_state.state)
        if u is not None:
            self._entities[game_element_state.name] = u

    @final
    def _add(self, game_element_state: GameElementState):
        self._entities[game_element_state.name] = self.build_entity(game_element_state)

    @final
    def convert(self, state_wrapper):
        """
        Convert the game element, and update or add it in the state.
        :param state_wrapper: game element from the list receive.
        """
        ges = self._game_element_state_converter.convert(state_wrapper)
        if ges.name in self._entities:
            self._update(ges)
        else:
            self._add(ges)

    @abstractmethod
    def build_entity(self, game_element_state: GameElementState) -> IStateEntity:
        """
        Implements a way to redirect the building of game entities.
        Need to call build method from the implemented game entities.
        :param game_element_state:
        """
        raise NotImplementedError


def choose_delegate(value):
    if isinstance(value, bool):
        return EntityBoolAdapter(value)
    elif isinstance(value, int):
        return EntityIntAdapter(value)
    elif isinstance(value, float):
        return EntityFloatAdapter(value)
    elif isinstance(value, complex):
        return EntityComplexAdapter(value)
    elif isinstance(value, str):
        return EntityStrAdapter(value)
    elif isinstance(value, list):
        return EntityListAdapter(value)
    elif isinstance(value, tuple):
        return EntityTupleAdapter(value)
    elif isinstance(value, set):
        return EntitySetAdapter(value)
    elif isinstance(value, dict):
        if "__type__" in value:
            return EntityObject(value)
        return EntityDictAdapter(value)


class Entity(IStateEntity):

    def __hash__(self):
        raise NotImplementedError


class EntityDictAdapter(dict, Entity):

    def __init__(self, value):
        dict.__init__({})
        for k in value:
            if k != "__type__":
                if isinstance(value[k], Entity):
                    self[k] = value[k]
                else:
                    self[k] = choose_delegate(value[k])

    @staticmethod
    def build(state) -> IStateEntity:
        return EntityDictAdapter(state)

    def update_state(self, state):
        for k in state:
            if k in self:
                self[k] = self[k].update_state(state[k])
            else:
                self[k] = choose_delegate(state[k])
        return self

    def __hash__(self):
        return hash(tuple(self.keys()))


class EntityObject(EntityDictAdapter):

    def __init__(self, value):
        EntityDictAdapter.__init__(self, value)
        if "__type__" in value:
            self.__type__ = value["__type__"]

    @staticmethod
    def build(state) -> IStateEntity:
        return EntityObject(state)

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(f"'{self.__type__}' object has no attribute '{name}'")

    def update_state(self, state):
        for k in state:
            if k != "__type__":
                if k in self and isinstance(self[k], Entity):
                    self[k] = self[k].update_state(state[k])
                else:
                    self[k] = choose_delegate(state[k])
        return self


class EntityBoolAdapter(int, Entity):

    def __init__(self, value):
        bool.__init__(value)

    @staticmethod
    def build(state) -> IStateEntity:
        return EntityBoolAdapter(state)

    def update_state(self, state):
        return EntityBoolAdapter(state)

    def __hash__(self):
        return hash(bool(self))


class EntityIntAdapter(int, Entity):

    def __init__(self, value):
        int.__init__(value)

    @staticmethod
    def build(state) -> IStateEntity:
        return EntityIntAdapter(state)

    def update_state(self, state):
        return EntityIntAdapter(state)

    def __hash__(self):
        return hash(int(self))


class EntityFloatAdapter(float, Entity):

    def __init__(self, value):
        float.__init__(value)

    @staticmethod
    def build(state) -> IStateEntity:
        return EntityFloatAdapter(state)

    def update_state(self, state):
        return EntityFloatAdapter(state)

    def __hash__(self):
        return hash(float(self))


class EntityComplexAdapter(complex, Entity):

    def __init__(self, value):
        complex.__init__(value)

    @staticmethod
    def build(state) -> IStateEntity:
        return EntityComplexAdapter(state)

    def update_state(self, state):
        return EntityComplexAdapter(state)

    def __hash__(self):
        return hash(complex(self))


class EntityStrAdapter(str, Entity):

    def __init__(self, value):
        str.__init__(value)

    @staticmethod
    def build(state) -> IStateEntity:
        return EntityStrAdapter(state)

    def update_state(self, state):
        return EntityStrAdapter(state)

    def __hash__(self):
        return hash(str(self))


class EntityListAdapter(list, Entity):

    def __init__(self, value):
        list.__init__([])
        for i in value:
            if isinstance(i, Entity):
                self.append(i)
            else:
                self.append(choose_delegate(i))

    @staticmethod
    def build(state) -> IStateEntity:
        return EntityListAdapter(state)

    def update_state(self, state):
        self.clear()
        for i in state:
            if isinstance(i, Entity):
                self.append(i)
            else:
                self.append(choose_delegate(i))
        return self

    def __hash__(self):
        return hash(tuple(self))


class EntityTupleAdapter(tuple, Entity):

    def __init__(self, value):
        tuple.__init__((i if isinstance(i, Entity) else choose_delegate(i) for i in value))

    @staticmethod
    def build(state) -> IStateEntity:
        return EntityTupleAdapter(state)

    def update_state(self, state):
        return EntityTupleAdapter(state)

    def __hash__(self):
        return hash(tuple(self))


class EntitySetAdapter(set, Entity):

    def __init__(self, value):
        super().__init__()
        for i in value:
            self.add(i if isinstance(i, Entity) else choose_delegate(i))

    @staticmethod
    def build(state) -> IStateEntity:
        return EntitySetAdapter(state)

    def update_state(self, state):
        self.clear()
        for i in state:
            self.add(i if isinstance(i, Entity) else choose_delegate(i))
        return self

    def __hash__(self):
        return hash(tuple(self))


class AutoEntityManager(EntityManager):
    def build_entity(self, game_element_state: GameElementState) -> IStateEntity:
        if game_element_state.type == "unknown":
            if isinstance(game_element_state.state, int):
                return EntityIntAdapter.build(game_element_state.state)
            elif isinstance(game_element_state.state, bool):
                return EntityBoolAdapter.build(game_element_state.state)
            elif isinstance(game_element_state.state, dict):
                return EntityDictAdapter.build(game_element_state.state)
            elif isinstance(game_element_state.state, str):
                return EntityStrAdapter.build(game_element_state.state)
            elif isinstance(game_element_state.state, float):
                return EntityFloatAdapter.build(game_element_state.state)
            elif isinstance(game_element_state.state, list):
                return EntityListAdapter.build(game_element_state.state)
            elif isinstance(game_element_state.state, tuple):
                return EntityTupleAdapter.build(game_element_state.state)
            elif isinstance(game_element_state.state, set):
                return EntitySetAdapter.build(game_element_state.state)
            elif isinstance(game_element_state.state, complex):
                return EntityComplexAdapter.build(game_element_state.state)
            else:
                raise ValueError(f"Unknown type {type(game_element_state.state)}")
        return EntityObject.build(game_element_state.state)

    def __getattr__(self, item):
        if item in self._entities:
            return self._entities[item]
        raise AttributeError
