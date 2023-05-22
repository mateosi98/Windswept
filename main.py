from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.base_class import BaseAlgorithm

from env import WindSweptEnv


def set_seed(env: WindSweptEnv, seed: int = 0):
    set_random_seed(seed)
    env.seed(seed)
    env.observation_space.seed(seed)
    env.action_space.seed(seed)


def eval_model(model: BaseAlgorithm, num_evals: int = 100):
    env = WindSweptEnv()
    set_seed(env, seed=1)
    total_steps_completed, total_moves_used, failed_episodes = 0, 0, 0
    for _ in range(num_evals):
        state, done, step, moves = env.reset(), False, 0, 1
        while not done and step < 100:
            action = model.predict(state)[0]
            state, _, done, info = env.step(action)
            if info['wind-has-blown'] and not done:
                moves += 1
            step += 1
        if step < 100:
            total_steps_completed += step
            total_moves_used += moves
        else:
            failed_episodes += 1
    successful_episodes = num_evals - failed_episodes

    print()
    if successful_episodes > 0:
        print(f'Average number of bricks placed to complete an episode: '
            f'{total_steps_completed / (successful_episodes):.2f}')
        print(f'Average number of moves taken to complete an episode: '
            f'{total_moves_used / (successful_episodes):.2f}')
    print(f'Number of times the agent was not able to complete the episode: '
          f'{failed_episodes}')
