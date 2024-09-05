from xumes.core.singleton import singleton


@singleton
class ParametersRegistry:
    """
    A class to store parameters in a dictionary-like structure.
    This class is a singleton, so it should be used as a global object.
    """

    def __init__(self):
        self._parameters = {}

    def register(self, name, value):
        self._parameters[name] = value

    def get(self, name):
        if name in self._parameters:
            return self._parameters[name]
        else:
            return None

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, name, value):
        self.register(name, value)

    def __contains__(self, name):
        return name in self._parameters

    def __iter__(self):
        return iter(self._parameters)

    def __len__(self):
        return len(self._parameters)

    def __str__(self):
        return str(self._parameters)

    def __repr__(self):
        return repr(self._parameters)

    def __eq__(self, other):
        if not isinstance(other, ParametersRegistry):
            return False

        return self._parameters == other._parameters

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._parameters)
