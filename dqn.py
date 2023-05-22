from stable_baselines3 import DQN

from env import WindSweptEnv
from common import eval_model, set_seed


def train_dqn(log_to_tensorboard: bool = False) -> DQN:
    env = WindSweptEnv()
    set_seed(env)
    tb_log_dir = './logs/DQN' if log_to_tensorboard else None
    model = DQN('MlpPolicy', env, verbose=1, tensorboard_log=tb_log_dir)
    model.learn(total_timesteps=500_000)
    return model


def main():
    dqn_model = train_dqn(log_to_tensorboard=True)
    eval_model(dqn_model)


if __name__ == '__main__':
    print()
    main()
