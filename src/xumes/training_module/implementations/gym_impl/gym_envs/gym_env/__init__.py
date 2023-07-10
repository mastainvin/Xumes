from gymnasium.envs.registration import register

register(
    id="xumes-v0",
    entry_point="gym_env.gym_adapter_env.gym_adapter:GymAdapter",
)
