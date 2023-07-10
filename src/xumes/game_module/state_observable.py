from __future__ import annotations

import copy
import functools
import logging
import types
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import TypeVar, Generic, final, List, Dict, Union, Tuple, Any

from xumes.game_module.errors.state_conversion_error import StateConversionError
from xumes.game_module.game_element_state import GameElementState
from xumes.game_module.i_game_state_observer import IGameStateObserver

OBJ = TypeVar("OBJ")
ST = TypeVar("ST")


class StateObservable(Generic[OBJ, ST], ABC):
    """
    The `StateObservable` class is an abstract base class for observable game states.

    Attributes:
        _observers: A list of `IGameStateObserver` instances subscribed to the observable.
        _object: The observable object.
        _name: The name of the observable.

    Methods:
        attach(observer): Attaches an observer to the observable.
        detach(observer): Detaches an observer from the observable.
        detach_all(): Detaches all observers from the observable.
        notify(): Notifies all observers of a state change.
        state(): Provides a representation method of a game element state.
        name: Property representing the name of the observable.
        observers: Property representing the list of observers.
        object: Property representing the observable object.
    """

    def __init__(self, observable_object: OBJ, observers: IGameStateObserver | List[IGameStateObserver], name: str):
        self._observers: List[IGameStateObserver] = []
        self._object = observable_object
        self._name = name
        if isinstance(observers, List):
            for observer in observers:
                self.attach(observer)
        else:
            self.attach(observers)

    @final
    def attach(self, observer: IGameStateObserver | List[IGameStateObserver]) -> None:
        """
        Attach method of the observable.
        :param observer: GameStateObserver implementation.
        """
        observers_temp = set(self._observers.copy())
        if isinstance(observer, List):
            for observer in observer:
                observers_temp.add(observer)
        else:
            observers_temp.add(observer)
        self._observers.clear()
        self._observers.extend(list(observers_temp))

    @final
    def detach(self, observer: IGameStateObserver | List[IGameStateObserver]) -> None:
        """
        Detach method of the observable.
        :param observer: GameStateObserver implementation.
        """
        if isinstance(observer, List):
            for observer in observer:
                if observer in self._observers:
                    observer.remove_state(self)
                    self._observers.remove(observer)
        else:
            if observer in self._observers:
                observer.remove_state(self)
                self._observers.remove(observer)

    @final
    def detach_all(self):
        """
        Detach every observer, we used this method when we want to
        destroy the object.
        """
        if self._observers is not None and self._observers:
            for observer in self._observers:
                observer.remove_state(self)

        self._observers.clear()

    @final
    def notify(self):
        """
        Notify method of the observable.
        TODO : Add a parameter to notify only a specific attribute change.
        As this: notify("attribute_name")
        Then we update state only for this attribute.
        """
        if self._observers is not None and self._observers:
            for observer in self._observers:
                observer.update_state(self)

    def state(self) -> GameElementState[ST]:
        """
        Give a representation method of a game element state.
        Mandatory for every class we want to observe.
        """
        raise NotImplementedError

    @property
    @final
    def name(self) -> str:
        return self._name

    @final
    @property
    def observers(self):
        return self._observers

    @final
    @property
    def object(self):
        return self._object


class State:
    """
    The `State` class is a representation of a game state.
    We use this class as a composite pattern to represent a game state.
    We can use this class to represent a game state with multiple attributes which are States.

    Attributes:
        name: The name of the state.
        attributes: The attributes of the state.
        func: The function to call when we retrieve the state.
    """

    def __init__(self, name: str = None, attributes: List[State] | State | str | List[str] = None, func=None,
                 methods_to_observe: List[str] | str = None):
        self.name = name
        self.func = func

        if isinstance(methods_to_observe, str):
            methods_to_observe = [methods_to_observe]

        self.methods_to_observe = methods_to_observe

        if isinstance(attributes, str):
            attributes = State(attributes)
        elif isinstance(attributes, list):
            for i in range(len(attributes)):
                if isinstance(attributes[i], str):
                    attributes[i] = State(attributes[i])

        self.attributes = attributes

    def __eq__(self, other):
        if self.name != other.name:
            return False

        if self.func is not None and other.func is not None:
            if self.func.__code__.co_code != other.func.__code__.co_code:
                return False

        if self.methods_to_observe is not None and other.methods_to_observe is not None:
            if len(self.methods_to_observe) != len(other.methods_to_observe):
                return False
            for i in range(len(self.methods_to_observe)):
                if self.methods_to_observe[i] != other.methods_to_observe[i]:
                    return False
        elif self.methods_to_observe is None and other.methods_to_observe is not None:
            return False
        elif self.methods_to_observe is not None and other.methods_to_observe is None:
            return False

        if isinstance(self.attributes, State):
            self.attributes = [self.attributes]
        if isinstance(other.attributes, State):
            other.attributes = [other.attributes]
        if self.attributes is not None and other.attributes is not None:
            if isinstance(self.attributes, list) and isinstance(other.attributes, list):
                if len(self.attributes) != len(other.attributes):
                    return False
                for i in range(len(self.attributes)):
                    if self.attributes[i] != other.attributes[i]:
                        return False
            elif isinstance(self.attributes, State) and isinstance(other.attributes, State):
                if self.attributes != other.attributes:
                    return False
            else:
                return False
        elif self.attributes is None and other.attributes is not None:
            return False
        elif self.attributes is not None and other.attributes is None:
            return False
        return True

    def __hash__(self):
        h = []
        if self.attributes is not None:
            for attr in self.attributes:
                if isinstance(attr, State):
                    h.append(hash(attr.name))
        return hash((self.name, self.func, tuple(h), tuple(self.methods_to_observe)))

    def __copy__(self):
        return State(self.name, self.attributes, self.func, self.methods_to_observe)

    def __deepcopy__(self, memodict={}):
        return State(self.name, copy.deepcopy(self.attributes, memodict), self.func, self.methods_to_observe)


def get_object_from_attributes(obj, attributes: List[State] | State | List[str] | str = None):
    """
    Convert an object to a dict object from attributes.

    :param obj: The object from which to retrieve attributes.
    :param attributes: The attributes to retrieve from the object. Can be a single attribute name (str),
                       a list of attribute names (List[str]), a State object, or a list of State objects.
                       Default is None, which retrieves the object itself.
    :return: The dict form of the object with the specified attributes.

    :raises StateConversionError: If there is an error in attribute conversion or the specified attribute
                                  is not found in the object.
    """

    # If the object a primitive type, return it
    if isinstance(obj, (int, str, bool, float, complex, bytes, bytearray, memoryview, set, frozenset)):
        return obj

    # Convert attributes to a list of State objects if it is a list of strings
    if isinstance(attributes, list):
        for i in range(len(attributes)):
            if isinstance(attributes[i], str):
                attributes[i] = State(attributes[i])

    # Convert attributes to a State object if it is a string
    if isinstance(attributes, str):
        attributes = State(attributes)

    # If there is just one attribute
    if isinstance(attributes, State) or attributes is None:

        # Get func if exists
        if attributes is not None and attributes.func is not None:
            func = attributes.func
        else:
            func = None

        # If list with get attributes from all element of the list and apply the function on the result
        if isinstance(obj, list):
            if func:
                try:
                    return func([get_object_from_attributes(o, attributes) for o in obj])
                except Exception:
                    raise StateConversionError("Error in function : " + str(func))

            return [get_object_from_attributes(o, attributes) for o in obj]
        # If tuple with get attributes from all element of the tuple and apply the function on the result
        elif isinstance(obj, tuple):
            if func:
                try:
                    return func(tuple([get_object_from_attributes(o, attributes) for o in obj]))
                except Exception:
                    raise StateConversionError("Error in function : " + str(func))
            return tuple([get_object_from_attributes(o, attributes) for o in obj])
        # If range just return the range
        elif isinstance(obj, range):
            return range(obj.start, obj.stop)
        # If dict with get attributes from all element of the dict and apply the function on the result
        elif isinstance(obj, dict):
            if func:
                try:
                    return func({k: get_object_from_attributes(v, attributes) for k, v in obj.items()})
                except Exception:
                    raise StateConversionError("Error in function : " + str(func))
            return {k: get_object_from_attributes(v, attributes) for k, v in obj.items()}

        # If object with get attributes from all element of the object and apply the function on the result
        if attributes:
            try:
                attributes_dict = {
                    attributes.name:
                        attributes.func(get_object_from_attributes(
                            getattr(obj, attributes.name), attributes.attributes))
                        if attributes.func else
                        get_object_from_attributes(
                            getattr(obj, attributes.name), attributes.attributes),
                    "__type__": obj.__class__.__name__}
                return attributes_dict
            except AttributeError:
                raise StateConversionError("Attribute " + attributes.name + " not found in object " + str(obj))
        else:
            return obj

    # If there is a list of attributes
    if isinstance(attributes, List):

        def create_dict(o, attrs):
            d = {
                attribute.name: attribute.func(
                    get_object_from_attributes(getattr(o, attribute.name), attribute.attributes))
                if attribute.func else get_object_from_attributes(getattr(o, attribute.name), attribute.attributes)
                for attribute in attrs
            }
            d["__type__"] = o.__class__.__name__
            return d

        # If list with get attributes from all element of the list and apply the function on the result
        if isinstance(obj, list):
            attributes_dict = [
                create_dict(element, attributes)
                for element in obj
            ]
        # If tuple with get attributes from all element of the tuple and apply the function on the result
        elif isinstance(obj, tuple):
            attributes_dict = [
                create_dict(element, attributes)
                for element in obj
            ]
            attributes_dict = tuple(attributes_dict)
        # If range just return the range
        elif isinstance(obj, range):
            attributes_dict = range(obj.start, obj.stop)
        # If dict with get attributes from all element of the dict and apply the function on the result
        elif isinstance(obj, dict):
            attributes_dict = {
                k: create_dict(v, attributes)
                for k, v in obj.items()
            }
        # If object with get attributes from all element of the object and apply the function on the result
        else:
            try:
                attributes_dict = {
                    attribute.name: attribute.func(get_object_from_attributes(getattr(obj, attribute.name), attribute.attributes)) if attribute.func else get_object_from_attributes(getattr(obj, attribute.name), attribute.attributes) for
                    attribute in attributes}
                attributes_dict["__type__"] = obj.__class__.__name__
            except AttributeError as e:
                raise StateConversionError(str(e) + " in object " + str(obj))
        return attributes_dict


class GameStateObservable(StateObservable[OBJ, ST]):
    __slots__ = ('_state', '_object', '_observers', '_name', '_methods_to_observe', '_update', '_attributes')

    def __init__(self, observable_object: OBJ, name: str,
                 observers: IGameStateObserver | List[IGameStateObserver] = None,
                 state: List[State] | State | str | List[str] = None,
                 ):

        self._methods_to_observe: Dict[str, List[State]] = {}  # Dict of methods to observe
        self._update = None  # Last method called
        self._attributes: Dict[str, List[str]] = {}  # Attributes to observe
        if observers is None:
            observers = []
        super().__init__(observable_object, observers, name)
        self._state = []
        self.set_state(state)
        self.notify()

    def state(self) -> GameElementState[ST]:
        """
        Give a representation method of a game element state.
        Here it is a dictionary with the attributes of the object.
        """
        return GameElementState(get_object_from_attributes(self._object, self._state if not self._update else
        self._methods_to_observe[self._update]))

    def _in_slots(self, attr) -> bool:
        """
        Check if the attribute is in the slots of the object
        :param attr: str attribute name
        :return: if the attribute is in the slots
        """
        for cls in type(self).__mro__:
            if attr in getattr(cls, '__slots__', []):
                return True
        return False

    def __getattr__(self, attr):
        """
        Delegate the get attribute to the object and notify the observers.
        :param attr: attribute name
        :return: the attribute
        """

        if self._in_slots(attr):
            return object.__getattr__(self, attr)
        value = getattr(self._object, attr)

        if callable(value) and attr in self._methods_to_observe:
            def wrapped_method(*args, **kwargs):
                result = value(*args[1:], **kwargs)
                logging.debug("Notify observers of " + self._name + " for method " + attr)
                self._update = attr
                self.notify()
                self._update = None
                return result

            return types.MethodType(wrapped_method, self)

        return value

    def __setattr__(self, attr, value):
        """
        Delegate the set attribute to the object and notify the observers.
        :param attr: attribute name
        :param value: value to set
        """
        if self._in_slots(attr):
            object.__setattr__(self, attr, value)
            return
        setattr(self._object, attr, value)
        if attr in self._attributes:
            logging.debug("Notify observers of " + self._name + " for attribute " + attr)
            if self._attributes[attr]:
                self._update = self._attributes[attr][0]
            else:
                self._update = None
            self.notify()
            self._update = None

    @final
    def set_state(self, attributes: List[State] | State | str | List[str]):
        """
        Convert the attributes to a list of State and set the state.
        :param attributes: attributes to set
        """

        # Convert attributes to a list of State
        if isinstance(attributes, str):
            attributes = State(attributes)
        if isinstance(attributes, List):
            for i in range(len(attributes)):
                if isinstance(attributes[i], str):
                    attributes[i] = State(attributes[i])
        if isinstance(attributes, State):
            self._state = [attributes]
        else:
            self._state = attributes

        def fill_methods_to_observe(states: List[State] | State):
            """
            Create a dict of methods to observe in keys and the states to observe in values.
            :param states: states to observe (recursive)
            """
            if isinstance(states, State):
                states = [states]

            if states:
                for state in states:
                    if state.methods_to_observe:
                        for method in state.methods_to_observe:
                            if method not in self._methods_to_observe:
                                self._methods_to_observe[method] = [state]
                            else:
                                self._methods_to_observe[method].append(state)
                    if state.attributes:
                        fill_methods_to_observe(state.attributes)

        fill_methods_to_observe(self._state)

        # Find the state to observe for each method
        # Using a dfs to find the state to observe for each method
        for method in self._methods_to_observe:
            self._methods_to_observe[method] = self._find_state(self._methods_to_observe[method])

        def fill_attributes(states: List[State] | State):
            """
            Create a list of attributes to observe.
            :param states: states to observe (recursive)
            """
            if isinstance(states, State):
                states = [states]

            if states:
                for state in states:
                    self._attributes[state.name] = state.methods_to_observe
                    if state.attributes:
                        if isinstance(state.attributes, State):
                            state.attributes = [state.attributes]
                        for attribute in state.attributes:
                            fill_attributes(attribute)

        fill_attributes(self._state)

    def _find_state(self, ends: List[State]) -> List[State] | None:
        """
        Find the state to observe for each method.
        :param ends: states to observe
        :return: The state tree to observe
        :raise ValueError: if the state is not in the object
        """
        if not ends:
            return self._state

        def dfs(node):
            if node is None:
                return False

            if node in ends:
                return True
            is_in = False
            if node.attributes:
                to_remove = []
                if isinstance(node.attributes, State):
                    node.attributes = [node.attributes]
                for s in node.attributes:
                    if not dfs(s):
                        to_remove.append(s)
                    else:
                        is_in = True
                for s in to_remove:
                    node.attributes.remove(s)
            return is_in

        node = State(attributes=copy.deepcopy(self._state))

        if not dfs(node):
            raise ValueError("The state is not in the object")
        return node.attributes
