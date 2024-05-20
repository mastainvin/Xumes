# from xumes.behavior.trainer_manager import observation, reward, action, config, terminated, StableBaselinesTrainerManager, VecStableBaselinesTrainerManager, TrainerManager

from xumes.behavior.behavior import Behavior

from gymnasium.envs.registration import register

register(
    id="xumes-v0",
    entry_point="xumes.behavior.implementations.gym_impl.gym_envs.gym_env.gym_adapter_env.gym_adapter:GymAdapter",
)
