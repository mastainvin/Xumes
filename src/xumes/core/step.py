import dill


class Step:

    def __init__(self, func, content, params=None):
        self.func = func
        self.content = content
        if params is None:
            params = {}
        self.params = params

    def add_params(self, scenario_name, params):
        self.params[scenario_name] = params

    def __reduce__(self):
        return self.__class__, (self.func, self.content, self.params)
