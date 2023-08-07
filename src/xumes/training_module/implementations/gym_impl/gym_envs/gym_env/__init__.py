from gymnasium.envs.registration import register
import gymnasium

if 'xumes-v0' not in gymnasium.registry:
    register(
        id="xumes-v0",
        entry_point="gym_env.gym_adapter_env.gym_adapter:GymAdapter",
    )
