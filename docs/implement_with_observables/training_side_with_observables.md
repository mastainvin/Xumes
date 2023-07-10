# Training side

## Description


The training side is the part of the framework that will train the model to predict the actions from the game states.

You will need to implement three types of classes:

- `IEntity`: This will give a minimalist representation of a game element state.
- `EntityManager`: This will handle the build of Entities.
- `TrainingService`: This will handle the training of the model.

## Implementation

### 1. IEntity and EntityManager

For every class that you observe in the game, you need to create an `IEntity` with the corresponding attributes.

For example, if you have a class called `Entity`, the implementation of the `IEntity` class would be as follows:


```python
class Entity:

    def __init__(self, val1):
        self.attr1 = val1
        self.attr2 = val2
        ...

    def method1(self):
        ...

    def method2(self):
        ...
```

We need to create an `IEntity` class that will represent the state of the `Entity` class:

```python
class EntityEntity(IEntity):

    def __init__(self, val1):
        self.attr1 = val1

    def update(self, state) -> None:
        self.attr1 = state['attr1']

    @staticmethod
    def build(state) -> IEntity:
        return EntityEntity(state['attr1'])
```
The `update` method will be called by the framework to update the state of the `IEntity` object.
The `build` method will be called by the framework to build the `IEntity` object from a state.

The `EntityManager` will handle the build of `IEntity` objects:

```python
class GameEntityManager(EntityManager):

    def build_entity(self, game_element_state):
        if game_element_state.type == "Entity":
            return EntityEntity.build(game_element_state.state)
```

### 2. TrainingService

The `TrainingService` will handle the training of the model. If you want to use the `stablebaselines` implementation, you will need to extend the `StableBaselinesTrainer` class like this:


```python
class GameTrainingService(StableBaselinesTrainer):

    def __init__(self, game_entity_manager: EntityManager, game_state_manager: StateManager, game_action_manager: ActionManager):
        super().__init__(game_entity_manager, game_state_manager, game_action_manager)


```

Then you need to implement four methods:

- `convert_obs`: This method will return the observation of the game state and extract the features.
- `convert_actions`: This method will convert the output of the model to a game action.
- `convert_terminated`: This method will convert the observation of the game state to a boolean that indicates if the game is terminated.
- `convert_reward`: This method will convert the observation of the game state to a reward.

You can use those methods to help you:

- `self.get_entity(str: name)`: This method will return the `IEntity` object corresponding to the name.
- `self.game_state`: This attribute will return the current game state.

Here's an example of implementation:

```python
    def convert_obs(self):
        return {"entity": np.array([self.get_entity("entity").attr1])}

    def convert_actions(self, actions):
        if actions == 0:
            return ["space"]
        return ["nothing"]

    def convert_terminated(self):
        return self.game_state == "lose"

    def convert_reward(self):
        return 1 if self.game_state == "win" else 0
```

### Use the TrainingService

To use the `TrainingService`, you need to create a `GameTrainingService` object and call the `train` method:

The `TrainingService` class needs two parameters:

- `entity_manager`: This is the `EntityManager` object that you created.
- `communication_service`: This is a `CommunicationService` object that will handle the communication with the game side. You can use the `CommunicationServiceTrainingMq` class.

When you are using `stablebaselines`, you will need to pass more parameters:

- `observation_space`
- `action_space`
- `max_episode_length`
- `total_timesteps`
- `algorithm_type`
- `algorithm`

Check the `stablebaselines` [documentation](https://stable-baselines3.readthedocs.io/en/master/) for more information.
Here's an example of implementation:
```python
training_service = GameTrainingService(
        entity_manager=GameEntityManager(
            JsonGameElementStateConverter()
        ),
        communication_service=CommunicationServiceTrainingMq(),
        observation_space=spaces.Dict({
                "entity": spaces.Box(0, 1, shape=(1, ), dtype=float),
        }),
        action_space=spaces.Discrete(2),
        max_episode_length=2000,
        total_timesteps=int(2e5),
        algorithm_type="MultiInputPolicy",
        algorithm=stable_baselines3.PPO
    )
```

If you want to train the model, you can call the `train` method. This will start the training process and update the model based on the provided training data.

To load a pre-trained model, you can use the `load` method by providing the path to the saved model as a parameter. This will load the model weights and configuration for further use.

If you want to make the agent play without training, you can call the `play` method. This will use the current model to make decisions and interact with the game environment based on its learned behavior.

To save the trained model, you can call the `save` method and provide the desired path where you want to save the model. This will store the model's weights and configuration for future use.

These methods provide flexibility in training, utilizing pre-trained models, playing the game, and saving the trained model for later use.