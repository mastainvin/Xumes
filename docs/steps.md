Steps files
===========


The steps files are responsible for implementing the tests that will be executed by the framework. They are written in
Gherkin, a language that allows you to write tests in a human-readable format. The framework will execute these tests by
interacting with the game through the game side component.

Each step file while require to implement the following methods using python decorators:

- `@given`: This method will be executed before each test. It is responsible for setting up the game state before the
  test starts.
- `@when`: This method will be executed just before the game loop. It is responsible for setting up the game state
  before the game loop starts.
- `@loop`: This method will be executed at each iteration of the game loop. It is responsible for executing the actions
  predicted by the training side and updating the game state.
- `@then`: This method will be executed after the game loop. It is responsible for asserting the expected game state
  after the test is finished.
- `@log`: This method will be executed after each iteration of the game loop. It is responsible for logging the game
  state if you want the game to be logged.
- `@render` [Optional if no render]: This method will be executed after each iteration of the game loop. It is
  responsible for rendering the game state if you want the game to be rendered.
- `@delete_screen` [Optional]: This method will be executed before the test. It is responsible for deleting the screen
  if possible.

> **_NOTE:_** The `given`, `when` and `then` decorators can handle arguments. 

The following diagram illustrates the execution flow of the steps files:

![steps](schemas/steps_files_schema.png)

## 1. `@given`

This method will instantiate the game and set up the game state before the test starts.
You will need to define each variable that we want to observe during the training process.
An observable is a variable that will notify his updates during the game loop. The framework will use these updates to
train the agent.

To observe a variable, you have two options:

- create an observable
- bind an object to an observable

### Create an Observable

To create an observable, you have to use `test_context.create()` method.

#### Parameters

| Parameter   | Type                           | Description                                       |
|-------------|--------------------------------|---------------------------------------------------|
| constructor | ObjType                        | The type of the object to observe.                |
| name        | str                            | The name of the observable.                       |
| state       | State   \| List[State] \| None | The state of the observable.                      |
| *args       | Any                            | The arguments to pass to the constructor.         |
| **kwargs    | Any                            | The keyword arguments to pass to the constructor. |

#### Return

| Type                   | Description              |
|------------------------|--------------------------|
| ObservableClassWrapper | The game object wrapped. |

### Bind an Object to an Observable

To bind an object to an observable, you have to use `test_context.bind()` method.

#### Parameters

| Parameter | Type                           | Description                  |
|-----------|--------------------------------|------------------------------|
| object    | ObjType                        | The object to observe.       |
| name      | str                            | The name of the observable.  |
| state     | State   \| List[State] \| None | The state of the observable. |

#### Return

| Type                        | Description                                                                  |
|-----------------------------|------------------------------------------------------------------------------|
| ComposedGameStateObservable | A observable that will redirect call to the inner object through reflection. |

Here is an example of a `@given` method:

```python
@given('the game is set up')
def test_impl(test_context):
    test_context.game = Game()
    test_context.game.player = test_context.create(Player, 'player', state=State('position'), position=(0, 0))
    test_context.game.enemy = test_context.bind(test_context.game.enemy, 'enemy', state=State('position'))
```

**When do we need to use `test_context.bind()`?**

When you want to observe an object that is already created by the game.
For instance, if you want to observe a list that is already created by the game.

**When do we need to use `test_context.create()`?**

When you want to observe an object that is not created by the game.
For instance, if you want to observe one object like the player.


> **_IMPORTANT:_** It's better to use `test_context.create()` because `test_context.bind()` is using reflection to call
> the
> methods of the inner object. That's mean you can lose some information about the object (like if the object is calling
> itself).

Ok but what is the state parameter?

### State

The purpose of the state is to represent the state of a game object. The state follows the Composite pattern, meaning it
can contain other states. The state representation should ultimately reach primitive types such as integers, floats,
strings, booleans, or collections of primitives.

| Parameter          | Type                           | Description                                  |
|--------------------|--------------------------------|----------------------------------------------|
| name               | str                            | The name of the atribute to get.             |
| attributes         | State   \| List[State] \| None | The list of attributes to get.               |
| func               | Callable       \| None         | The function to apply to the representation. |
| methods_to_observe | List[str]   \| str \| None     | The list of methods to observe.              |

Here is an example of a simple state that retrieves the attribute `a` of a game object.

```python
State("a")
```

You can also create more complex states that retrieve attributes from nested objects. For instance, the following state
retrieves the attribute `a` of the observed object with `b`, and `c` from the `a` object.

```python
State("a", [State("c"), State("b")])
```

> **_IMPORTANT:_** If you don't provide a representation of an object, the framework will return the object itself.
> That's mean you must either give a representation with `State` or give a `func` to `State` to represent the object as
> in
> the example at the bottom.

#### Observing setters

When creating a `State`, you define attributes to observe. 
If an attribute of the Observable is set, the state will be updated and you don't need to use `methods_to_observe`.

```python
class A:
  
  def __init__(self):
    self.a = 0
      
  def update(self):
    self.a += 1

a = test_context.create(A, "a", State("a"))    
```

In this example, when `a.update()` is called, the state "a" will be updated even if we don't use `methods_to_observe`.

> **_INFO:_** This can be useful for primitives attributes.

> **_IMPORTANT:_** This is not working for deeper attributes. For instance, if you have `State("a", State("b"))`, the
> state "b" will not be updated if `a.b` is set, because `b` is not an attribute of `A` which is the observable.

#### Observing Methods

When creating a `State`, you can specify a list of methods to observe. An observed method is a method inside the game
object that can trigger state updates.

```python
self.obj = self.create(Obj, "obj", State("a", methods_to_observe=["method"]))
```

In this example, when the `self.obj.method` is called, the state "a" will be updated.


> **_IMPORTANT:_** `methods_to_observe` are methods of the Observable.
```python
class A:
    def __init__(self):
        self.b = B()
 
    def method_a(self):
        self.b.method_b()
class B:
    def method_b(self):
        self.c=0

a = test_context.create(A, "a", State("b", State("c", methods_to_oberve="method_a")))
```

In this example, when `a.method_a()` is called, the state "c" will be updated. And you **can't** observe `method_b` because
it's not a method of `A`.


You can be more specific and provide a list of observed methods for each state.

```python
self.obj = self.create(Obj, "obj", State("a", State("b", methods_to_observe=["method", "method2"])))
```

Here, when `self.obj.method` or `self.obj.method2` are called, the state "b" will be updated.

> **_IMPORTANT:_** Be caution when choosing the methods to observe, specially if you are observing primitive types. For
> instance, if you observe a list, `li[0] = 1` doesn't trigger `__setitem__` as the non-primitive type does.

#### Representation Function

A `State` object can also have a representation function. This function is called whenever the state is updated,
allowing you to modify the state's representation.
To be more precise, the function is called on the result of the representation of the state's children.

To clarify, here is a list of different cases that can occur:

- If the child is an object without representation, the result is the object itself.
- If the child is an object with representation, the result is a `dict` object, where keys are attributes of the child
  object.
- If the child is a collection of objects without representation, the result is a collection of objects.
- If the child is a collection of objects with representation, the result is a collection of `dict` objects.
- If the child is a primitive type, the result is the value of the primitive type.

```python
self.obj = self.create(Obj, "obj", State("a", func=lambda x: x + 1))
```

In this example, when the "a" state is updated, the value will be incremented by 1 in its representation.

#### Observing Different Types of Attributes

The `bind` method supports observing different types of attributes:

- Objects (as seen before)
- Lists
- Dictionaries
- Tuples

Please note that you cannot directly observe `int`, `float`, `bool`, or `str` attributes because they require
re-instantiation when updated.

However, you can observe `list`, `dict`, and `tuple` attributes since they are mutable. If you want to re-instantiate
them, you'll need to rebind them using the `bind` method.

For example, let's say you have a list `self.my_list`, and you want to observe the attribute `a` of each object within
the list:

```python
self.my_list = self.bind(self.my_list, "my_list", State("a"))
```

> **_NOTE:_**
> We use `self.bind` instead of `self.create` because we want to observe an existing object.


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

#### More Complex Example

##### A real use case

Let's say you have an object `A` that contains a list of objects `B`. You want to observe the `b` attribute of each `B`
object while giving a representation of the `B` object just with its `b` value. And they are updated when the
method `update` of the `A` class is called.

```python
class A:
    def __init__(self, b_list):
        self.b_list = b_list

    def update(self):
        for b in self.b_list:
            b.update_state()


class B:
    def __init__(self, b):
        self.b = b

    def update(self):
        self.b += 1


self.a = A([B(1), B(2)])
```

You can achieve this as follows:

```python
self.a = self.bind(self.a, "a",
                   State("b_list", State("b", methods_to_observe=["update"]), func=lambda x: [b["b"] for b in x]))
```

or,

```python
self.a = self.bind(self.a, "a", State("b_list", func=lambda x: [b.b for b in x], methods_to_observe=["update"]))
```

Explanation:

In the first case, we provide a representation of every element of the `b_list`
with `State("b", methods_to_observe=["update"])`. So when we compute the representation of the `b_list`, we will have a
list of `dict` objects with the key `b` and the value of the `b` attribute of the `B` object. Then we provide a
representation function to the `b_list` state with `func=lambda x: [b["b"] for b in x]`.

In the second case, we provide a representation function to the `b_list` state with `func=lambda x: [b.b for b in x]`.
Since we didn't provide a representation of every element of the `b_list`, the representation returns all the `B`
objects. So we need to give a representation function to the `b_list` state to return a list of `b` attributes of
the `B` objects. Then we give a list of observed methods to the `b_list` state with `methods_to_observe=["update"]`.

In both cases you will be able to use the `b_list` attribute of the `A` object on the training side like this:

```python
self.a.b_list[0]  # returns 1
```

##### To completely understand

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
self.a = self.bind(self.a, "a", State("b_list", func=lambda x: [[c.c for c in b.c_list] for b in x]),
                   methods_to_observe=["update"])
```

Those representations are equivalent and will return the same result on the training side:

```python
self.a.b_list = [[1, 2], [3]]
```

## 2. `@when`

The `@when` decorator is used to define the conditions under which a test is executed.
As you can see on the schema, it will be executed every time a game is terminated.

```python
@when("The player is in the room with the monster")
def test_impl(test_context):
    test_context.monster.room = test_context.player.room
```

## 3. `@loop`

The `@loop` decorator is used to define the game loop of our test. It's useful to update the game.

```python
@loop
def test_impl(test_context):
    test_context.game.update_state()
```

## 4. `@then`

The `@then` decorator is used to define the conditions under which a test is successful.
As you can see on the schema, it will be executed every time a game is terminated.
You have a list of `assertion` functions that you can use to define your conditions.

```python
@then("The player killed the monster")
def test_impl(test_context):
    test_context.assert_true(test_context.monster.is_dead)
```

### Assertion functions

#### `assert_true`

```python
test_context.assert_true(test_context.monster.is_dead)
```

#### `assert_false`

```python
test_context.assert_false(test_context.monster.is_dead)
```

#### `assert_equal`

```python
test_context.assert_equal(test_context.player.alive, True)
```

#### `assert_not_equal`

```python
test_context.assert_not_equal(test_context.monster.alive, True)
```

#### `assert_greater`

```python
test_context.assert_greater(test_context.player.health, 0)
```

#### `assert_greater_equal`

```python
test_context.assert_greater_equal(test_context.player.health, 0)
```

#### `assert_less`

```python
test_context.assert_less(test_context.player.health, 100)
```

#### `assert_less_equal`

```python
test_context.assert_less_equal(test_context.player.health, 100)
```

#### `assert_between`

```python
test_context.assert_between(test_context.player.health, 0, 100)
```

#### `assert_not_between`

```python
test_context.assert_not_between(test_context.player.health, 0, 100)
```

## 5. `@render`

The `@render` decorator is used to define the rendering of the game. It's useful to see the game in action.

```python
@render
def test_impl(test_context):
    test_context.game.render()
```

## 6. `@delete_screen`

The `@delete_screen` decorator is used to delete the screen of the game. It's made to avoid space and compute waste but
it's not mandatory.

```python
@delete_screen
def test_impl(test_context):
    test_context.game.delete_screen()
```

## 7. `@log`

The `@log` decorator is used to log the game.

```python
@log
def test_impl(test_context):
    return {
        "player_health": test_context.player.health,
        "monster_health": test_context.monster.health
    }
```


