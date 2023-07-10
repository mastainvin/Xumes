# Xumes

## Documentation

You can find the documentation [here](https://xumes.readthedocs.io/).
## Installation
```commandline
pip install -i https://test.pypi.org/simple/ xumes
```

It's possible that certain dependencies will not be found on test.pypi.org so you may have to install them yourself.

## Schema
![framework schema](https://github.com/mastainvin/Xumes/blob/main/schema.jpg?raw=true)

## Future work
- [ ] Add observable wrapper on game class attribut in order to get only the small changes and not all the object state.
- [ ] Add render mode with the same use as Gym.
- [ ] Remove the observers list in the TestRunner class.
- [ ] Add a Logger that contains GameServices and handles their changing state and their saving.