from gymnasium.envs.registration import register

register(
    id="xumes-v0",
    entry_point="xumes.modules.reinforcement_learning.gym_impl.gym_envs.gym_env.gym_adapter_env.gym_adapter:GymAdapter",
)
