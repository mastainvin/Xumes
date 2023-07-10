# Game Side

When working with the default observables implementation, you don't have to manually create game element observables. Instead, you can create a `TestRunner` class to handle it.

The state representation is a `dict` object.

The game loop object is not a different observable now, and you don't have access to the `update_state` method.
Now the game loop object is an `Observable` that you will have to bind to the `TestRunner` using the `bind` method.

## 1. Creating a TestRunner

To create a `TestRunner`, you need to define a class that inherits from the `TestRunner` base class.

```python
class MainTestRunner(TestRunner):
```

> **_NOTE:_** `MainTestRunner` doesn't inherit from the game loop class anymore.


Next, implement the `__init__` method.

```python
def __init__(self):
    super().__init__()
```

Inside the `__init__` method, bind your game state objects using the `bind` method.

```python
self.game_object1 = self.bind(self.game_object1, "name_game_object1", state)
```

The `bind` method takes three parameters: the game object, the name of the game object, and the associated state. The name is used to identify the game object on the training side.

## 2. State

The purpose of the state is to represent the state of a game object. The state follows the Composite pattern, meaning it can contain other states. The state representation should ultimately reach primitive types such as integers, floats, strings, booleans, or collections of primitives.

Here is an example of a simple state that retrieves the attribute `a` of a game object.

```python
State("a")
```

You can also create more complex states that retrieve attributes from nested objects. For instance, the following state retrieves the attribute `a` of the observed object with `b`, and `c` from the `a` object.

```python
State("a", [State("c"), State("b")])
```

> **_IMPORTANT:_** If you don't provide a representation of an object, the framework will return the object itself. That's mean you must either give a representation with `State` or give a `func` to `State` to represent the object as in the example at the bottom.

### Observing Methods

When creating a `State`, you can specify a list of methods to observe. An observed method is a method inside the game object that can trigger state updates.

```python
self.obj = self.bind(self.obj, "obj", State("a", methods_to_observe=["method"]))
```

In this example, when the `self.obj.method` is called, the state "a" will be updated.

You can be more specific and provide a list of observed methods for each state.

```python
self.obj = self.bind(self.obj, "obj", State("a", State("b", methods_to_observe=["method", "method2"])))
```

Here, when `self.obj.method` or `self.obj.method2` are called, the state "b" will be updated.

### Representation Function

A `State` object can also have a representation function. This function is called whenever the state is updated, allowing you to modify the state's representation.
To be more precise, the function is called on the result of the representation of the state's children.

To clarify, here is a list of different cases that can occur:

- If the child is an object without representation, the result is the object itself.
- If the child is an object with representation, the result is a `dict` object, where keys are attributes of the child object.
- If the child is a collection of objects without representation, the result is a collection of objects.
- If the child is a collection of objects with representation, the result is a collection of `dict` objects.
- If the child is a primitive type, the result is the value of the primitive type.

```python
self.obj = self.bind(self.obj, "obj", State("a", func=lambda x: x + 1))
```

In this example, when the "a" state is updated, the value will be incremented by 1 in its representation.

### Observing Different Types of Attributes

The `bind` method supports observing different types of attributes:

- Objects (as seen before)
- Lists
- Dictionaries
- Tuples

Please note that you cannot directly observe `int`, `float`, `bool`, or `str` attributes because they require re-instantiation when updated.

However, you can observe `list`, `dict`, and `tuple` attributes since they are mutable. If you want to re-instantiate them, you'll need to rebind them using the `bind` method.

For example, let's say you have a list `self.my_list`, and you want to observe the attribute `a` of each object within the list:

```python
self.my_list = self.bind(self.my_list, "my_list", State("a"))
```

In this case, for every element in `self.my_list`, the `a` attribute will be observed.

Consider a class `A`:

```python
class A:
    def __init__(self, a):
        self.a = a
```

If you have a list of `A` objects:

```python
self.my_list = [A(1), A(2), A(3)]
```

You will be able to access the `a` attribute of each `A` object within the list on the training side, like this:

```python
self.my_list[0].a
```

### More Complex Example

#### A real use case

Let's say you have an object `A` that contains a list of objects `B`. You want to observe the `b` attribute of each `B` object while giving a representation of the `B` object just with its `b` value. And they are updated when the method `update` of the `A` class is called.

```python
class A:
    def __init__(self, b_list):
        self.b_list = b_list

    def update(self):
        for b in self.b_list:
            b.update()

class B:
    def __init__(self, b):
        self.b = b

    def update(self):
        self.b += 1


self.a = A([B(1), B(2)])
```

You can achieve this as follows:

```python
self.a = self.bind(self.a, "a", State("b_list", State("b", methods_to_observe=["update"]), func=lambda x: [b["b"] for b in x]))
```
or,
```python
self.a = self.bind(self.a, "a", State("b_list", func=lambda x: [b.b for b in x], methods_to_observe=["update"]))
```

Explanation:

In the first case, we provide a representation of every element of the `b_list` with `State("b", methods_to_observe=["update"])`. So when we compute the representation of the `b_list`, we will have a list of `dict` objects with the key `b` and the value of the `b` attribute of the `B` object. Then we provide a representation function to the `b_list` state with `func=lambda x: [b["b"] for b in x]`.

In the second case, we provide a representation function to the `b_list` state with `func=lambda x: [b.b for b in x]`. Since we didn't provide a representation of every element of the `b_list`, the representation returns all the `B` objects. So we need to give a representation function to the `b_list` state to return a list of `b` attributes of the `B` objects. Then we give a list of observed methods to the `b_list` state with `methods_to_observe=["update"]`.


In both cases you will be able to use the `b_list` attribute of the `A` object on the training side like this:

```python
self.a.b_list[0] # returns 1
```

#### To completely understand

```python
class A:
    def __init__(self, b_list):
        self.b_list = b_list

class B:
    def __init__(self, c_list):
        self.c_list = c_list

class C:
    def __init__(self, c):
        self.c = c

self.a = A([B([C(1), C(2)]), B([C(3)])])
```


```python
self.a = self.bind(self.a, "a", State("b_list", 
                                 State("c_list", 
                                       State("c", methods_to_observe=["update"])), 
                                 func=lambda x: [[c["c"] for c in b["c_list"]] for b in x]))
```

```python
self.a = self.bind(self.a, "a", State("b_list", 
                                 State("c_list", methods_to_observe=["update"], 
                                       func=lambda x: [c.c for c in x]),      
                                 func=lambda x: [b["c_list"] for b in x]))
```

```python
self.a = self.bind(self.a, "a", State("b_list", func=lambda x: [[c.c for c in b.c_list] for b in x]), methods_to_observe=["update"])
```


Those representations are equivalent and will return the same result on the training side:

```python
self.a.b_list = [[1, 2], [3]]
```

## 3. Methods to implement


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
If you want to overwrite game entities, don't forget to `detach()` observers and rebind the observables.
```python
    def reset(self):
        self.entity.detach_all()
        self.entity = self.bind(...)
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

### Use the TestRunner

To use the TestRunner, you need to instantiate a `GameService` object and provide the TestRunner as a parameter:

```python
game_service = GameService(test_runner=MainTestRunner(),
                           event_factory=PygameEventFactory(),
                           communication_service=CommunicationServiceGameMq(ip="localhost"))
```

Once you have created the `GameService` object, you can start the test by calling `game_service.run()`. If you want to run the test with rendering, use `game_service.run_render()`.

Make sure to set the appropriate values for the `event_factory`, and `communication_service` parameters based on your specific requirements.

With these steps, you can utilize the TestRunner to perform testing on your game module.