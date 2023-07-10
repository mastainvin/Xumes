# Game side

## Description
To implement the game module, you need to create two types of objects:

- `StateObservable`: This will allow game objects to be observable in terms of their state.
- `TestRunner`: This will handle the implementation of test cases.

## Implementation

In our example we suppose that we have a game with one game element `Entity` and one unique game loop class named `Main`.

### 1. StateObservable

We need to implement the `StateObservable` class for the `Entity` object.

Here's the `Entity` class:

```python
class Entity:

    def __init__(self, val1):
        self.attr1 = val1
        self.attr2 = val2
        ...

    def method1(self, val):
        ...

    def method2(self):
        ...
```

#### Class creation
To create the `EntityObservable` class, we need to define a new adapter class that inherits from `Entity` and `StateObservable`. Make sure to extend from `Entity` first and then from `StateObservable`.

```python
class EntityObservable(Entity, StateObservable):
```

#### Constructor
The constructor of `EntityObservable` should include the parameters of `Entity` as well as observers and name.
```python
    def __init__(self, val1, observers, name):
        StateObservable.__init__(self, observable_object=self, observers=observers, name=name)
        Entity.__init__(self, val1)  # Initialise Entity with its parameters
        self.notify()
```

#### State modification notification
To notify the framework when an object changes its state, you need to overload every method that modifies the state. Call the corresponding method of `Entity` and then notify the observers.
```python
    def method1(self, val):
        Entity.method1(self, val)
        self.notify()
```

#### State representation
Implement a method to represent the state of the object. You can use dictionaries for now.
```python
    def state(self):
        return GameElementState({
            "attr1": self.attr1,
            "attr2": self.attr2
        })
```

#### EntityObservable's implementation
Here's the complete code for the `EntityObservable` class:

```python
class EntityObservable(Entity, StateObservable):
    def __init__(self, val1, observers, name):
        StateObservable.__init__(self, observable_object=self, observers=observers, name=name)
        Entity.__init__(self, val1)
        self.notify()
        
    def method1(self):
        Entity.method1(self)
        self.notify()

    def state(self):
        return GameElementState({
            "attr1": self.attr1,
            "attr2": self.attr2
        })
```

### 2. TestRunner

Let's suppose the `Main` is implemented like this:

```python
class Main:

    def __init__(self):
        self.entity = Entity(val1)
        ...

    def game_method1(self):
        ...
    
    def game_method2(self):
        ...

    def run(self):
        while self.running:
            self.game_method1()
            self.game_method2()
```

#### Class creation

As observables, the `MainTestRunner` class needs to inherit from `Main` and an implementation of `TestRunner`. 
You can use `JsonTestRunner` as it provides a representation of states in a dictionary.

```python
class MainTestRunner(Main, JsonTestRunner):
```

#### Class constructor

The implementation is nearly the same as the observables. You just have to **override** the game entities to use their observable representation.
> **_NOTE:_**  The constructors are inverted.

```python
    def __init__(self, observers):
        Main.__init__(self)
        JsonTestRunner.__init__(self, game_loop_object=self, observers=observers)

        self.entity = EntityObservable(val1=..., name="entity", observers=observers)
```


#### State modification notification

Similar to the game observables, you need to notify when the global game state changes. For example, when the player wins or loses. 
In our example, the `game_method1()` causes the player to lose, so we **overload** the method and notify the change.

```python
    def game_method1(self):
        Main.game_method1(self)
        self.update_state("lose")
```

If you want to insert notifications inside code, you need to **override** the method and copy the game code inside.

```python
    def game_method2(self):
        self.entity.method1()
        self.update_state("get_point")
        self.entity.method2()
```

#### run_test() implementation
The main method of the test runner is used to implement the test's game loop. Here, you don't need to render images or perform unnecessary computations.
```python
    def run_test(self):
        while self.running:
            self.test_client.wait()  # Very important line
            ...
            # game loop
            ...
```

#### run_test_render() implementation
This is the same as `run_test()`, but you need to implement a way to render images.
```python
    def run_test_render(self):
        while self.running:
            self.test_client.wait()  # Very important line
            ...
            # game loop
            self.render()
            ...
```

#### reset() implementation
The reset implementation is used to restart the game. 
If you want to overwrite game entities, don't forget to `detach()` observers and use the `StateObserver`.
```python
    def reset(self):
        self.entity.detach_all()
        self.entity = EntityObservable(val1=..., name="entity", observers=self.observers)
```

#### random_reset() implementation
The random reset is used to achieve faster and better convergence. You need to implement a way to set the game to a random state.
```python
    def random_reset(self):
        self.entity.val1 = random()
        self.entity.notify()
```

#### delete_screen() implementation
You don't need to implement it for now.


```python
    def delete_screen(self) -> None:
        pass
```


#### MainTestRunner implementation

Here's the complete code for the `MainTestRunner` class:


```python
class MainTestRunner(Main, JsonTestRunner):
    def __init__(self, observers):
        Main.__init__(self)
        JsonTestRunner.__init__(self, game_loop_object=self, observers=observers)

        self.entity = EntityObservable(val1=..., name="entity", observers=observers)

    def game_method1(self):
        Main.game_method1(self)
        self.update_state("lose")

    def game_method2(self):
        self.entity.method1()
        self.update_state("get_point")
        self.entity.method2()

    def run_test(self):
        while self.running:
            self.test_client.wait()  # Very important line
            ...
            # game loop
            ...

    def run_test_render(self):
        while self.running:
            self.test_client.wait()  # Very important line
            ...
            # game loop
            self.render()
            ...

    def reset(self):
        self.entity.detach_all()
        self.entity = EntityObservable(val1=..., name="entity", observers=self.observers)

    def random_reset(self):
        self.entity.val1 = random()
        self.entity.notify()

    def delete_screen(self) -> None:
        pass
```


### Use the TestRunner

To use the TestRunner, you need to instantiate a `GameService` object and provide the TestRunner as a parameter:

```python
game_service = GameService(observer=JsonGameStateObserver.get_instance(),
                                   test_runner=MainTestRunner(observers=[JsonGameStateObserver.get_instance()]),
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip="localhost"))
        
```

Once you have created the `GameService` object, you can start the test by calling `game_service.run()`. If you want to run the test with rendering, use `game_service.run_render()`.

Make sure to set the appropriate values for the `observer`, `event_factory`, and `communication_service` parameters based on your specific requirements.

With these steps, you can utilize the TestRunner to perform testing on your game module.