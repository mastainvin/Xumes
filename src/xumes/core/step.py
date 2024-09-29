import dill


class Step:
    def __init__(self, func, content, params=None):
        self.func = func
        self.content = content
        self.params = params if params else {}

    def add_params(self, scenario_name, parameters):
        if scenario_name not in self.params:
            self.params[scenario_name] = [parameters]
        else:
            self.params[scenario_name].append(parameters)


    def __reduce__(self):
        return self.__class__, (self.func, self.content, self.params)
