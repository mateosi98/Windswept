from sb3_contrib import TRPO

from env import WindSweptEnv
from common import eval_model, set_seed


def train_trpo(log_to_tensorboard: bool = False) -> TRPO:
    env = WindSweptEnv()
    set_seed(env)
    tb_log_dir = './logs/TRPO' if log_to_tensorboard else None
    model = TRPO('MlpPolicy', env, verbose=1, tensorboard_log=tb_log_dir)
    model.learn(total_timesteps=300_000)
    return model


def main():
    trpo_model = train_trpo(log_to_tensorboard=True)
    eval_model(trpo_model)


if __name__ == '__main__':
    print()
    main()
