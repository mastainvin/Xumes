
from xumes.training_module.i_state_entity import IStateEntity
from xumes.training_module.entity_manager import EntityManager
from xumes.training_module.entity_manager import AutoEntityManager
from xumes.training_module.implementations import *


from gymnasium.envs.registration import register

register(
    id="xumes-v0",
    entry_point="xumes.training_module.implementations.gym_impl.gym_envs.gym_env.gym_adapter_env.gym_adapter:GymAdapter",
)
