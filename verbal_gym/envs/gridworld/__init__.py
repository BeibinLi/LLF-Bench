from gymnasium.envs.registration import register
from verbal_gym.envs.gridworld.gridworld import Gridworld
from verbal_gym.envs.gridworld.wrapper import GridworldWrapper


ENVIRONMENTS = (
    'Gridworld-v0',
)


def make_env(env_name,
             instruction_type='b',
             feedback_type='r',
             ):

    """ Make the original env and wrap it with the VerbalGymWrapper. """
    env = Gridworld(instruction_type=instruction_type, feedback_type=feedback_type)
    # we don't pass arguments here, because _reset in BanditGymWrapper calls __init__ of the env without arguments.
    return GridworldWrapper(env, instruction_type=instruction_type, feedback_type=feedback_type)


for env_name in ENVIRONMENTS:
    # default version (backwards compatibility)
    register(
        id=f"verbal-{env_name}",
        entry_point='verbal_gym.envs.gridworld:make_env',
        kwargs=dict(env_name=env_name, feedback_type='a', instruction_type='b')
    )
