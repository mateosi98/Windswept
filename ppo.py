from stable_baselines3 import PPO

from env import WindSweptEnv
from common import eval_model, set_seed


def train_ppo(log_to_tensorboard: bool = False) -> PPO:
    env = WindSweptEnv()
    set_seed(env)
    tb_log_dir = './logs/PPO' if log_to_tensorboard else None
    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=tb_log_dir)
    model.learn(total_timesteps=300_000)
    return model


def main():
    ppo_model = train_ppo(log_to_tensorboard=True)
    eval_model(ppo_model)


if __name__ == '__main__':
    print()
    main()
