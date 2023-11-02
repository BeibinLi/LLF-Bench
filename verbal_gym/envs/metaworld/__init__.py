import gymnasium as gym
from gymnasium.envs.registration import register
from verbal_gym.utils import generate_combinations_dict
from verbal_gym.envs.metaworld.wrapper import MetaworldWrapper
from collections import defaultdict
import importlib
import metaworld
import random
import time
from gymnasium.wrappers import TimeLimit

BENCHMARK = metaworld.MT1
ENVIRONMENTS = tuple(BENCHMARK.ENV_NAMES)

def make_env(env_name,
             instruction_type='b',
             feedback_type='r',
             episode_length=20,
             ):
    """ Make the original env and wrap it with the VerbalGymWrapper. """
    benchmark = BENCHMARK(env_name)
    env = benchmark.train_classes[env_name]()
    class Wrapper(gym.Wrapper):
         # a small wrapper to make sure the task is set
         # and to make the env compatible with the old gym api
        def __init__(self, env):
            super().__init__(env)
            self.env.max_path_length = float('inf')
            # We remove the internal time limit. We will redefine the time limit in the wrapper.
        @property
        def env_name(self):
            return env_name
        def reset(self, *, seed=None, options=None):
            task = random.choice(benchmark.train_tasks)
            self.env.set_task(task)
            return self.env.reset(seed=seed, options=options)
    env = Wrapper(env)
    return TimeLimit(MetaworldWrapper(env, instruction_type=instruction_type, feedback_type=feedback_type), max_episode_steps=episode_length)


configs = generate_combinations_dict(
                dict(env_name=ENVIRONMENTS,
                     feedback_type=MetaworldWrapper.FEEDBACK_TYPES,
                     instruction_type=MetaworldWrapper.INSTRUCTION_TYPES))

for config in configs:
    env_name, version = config['env_name'].split('-v')
    register(
        id=f"verbal-{env_name}-{config['instruction_type']}-{config['feedback_type']}-v{version}",
        entry_point='verbal_gym.envs.metaworld:make_env',
        kwargs=config,
    )

for env_name in ENVIRONMENTS:
    # default version (backward compatibility)
    register(
        id=f"verbal-{env_name}",
        entry_point='verbal_gym.envs.metaworld:make_env',
        kwargs=dict(env_name=env_name, feedback_type='r', instruction_type='b')
    )