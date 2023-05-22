import gym
import numpy as np

from typing import Tuple, Dict, Any
from gym.spaces import MultiBinary, Discrete


class WindSweptEnv(gym.Env):
    """Class used to represent the WindSwept environment."""

    levels: int = 10
    max_bricks_per_level: int = 5
    max_moves: int = 3
    metadata: Dict[str, Any] = {'render.modes': []}
    reward_range: Tuple[float, float] = (-1, 0)

    def __init__(self) -> None:
        self.state: np.ndarray = None
        self.available_moves: int = -1
        self.observation_space = MultiBinary(self.input_shape)
        self.action_space = Discrete(self.levels)

    @property
    def input_shape(self) -> int:
        return self.levels * self.max_bricks_per_level + self.max_moves

    def _add_moves_and_flatten(self) -> np.ndarray:
        """Returns the flattened state along with the number of
            available moves information (concatenated)."""
        moves_arr = np.zeros(self.max_moves, dtype=np.uint8)
        moves_arr[:self.available_moves] = 1
        return np.concatenate((self.state.flatten(), moves_arr))

    def _blow_wind(self) -> None:
        """Randomly chooses a level and removes the rightmost brick
            of that level and all the bricks above it, if a brick exists."""
        # select a random level
        random_level = np.random.randint(0, self.levels)
        # if there are no bricks in that level, nothing happens
        if not self.state[random_level].any():
            return

        # else, there is at least 1 brick, find the rightmost
        for brick_pos in range(self.max_bricks_per_level):
            if self.state[random_level, brick_pos] == 0:
                actual_pos = brick_pos - 1

                # remove the brick and all of the bricks above it
                self.state[random_level, actual_pos] = 0
                for level_above in range(random_level + 1, self.levels):
                    self.state[level_above, actual_pos] = 0
                break

    def reset(self) -> np.ndarray:
        """Resets the state to an empty tower (no bricks on any level)
            and samples a number of moves to be made available."""
        self.state = np.zeros((self.levels, self.max_bricks_per_level),
                              dtype=np.uint8)
        self.available_moves = np.random.randint(1, self.max_moves + 1)
        return self._add_moves_and_flatten()

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict]:
        """Step on the environment:
            Add a brick to the rightmost part of the level.
                - If the level is maxed out on bricks, do nothing.
                - If the level is above ground (i.e. action > 0) and there is
                    no brick below, do nothing (brick can't "flow" on air).
            After the action has been performed, if it was the last available
                move for this round, the wind will blow in a random direction
                and the agent will get a new set of moves to act.
            The episode ends if at least one brick is placed at the last level.
        """
        # define the information dictionary
        info = {'wind-has-blown': False}

        # perform brick addition
        if self.state[action, -1] == 0:
            for brick_pos in range(self.max_bricks_per_level):
                if self.state[action, brick_pos] == 0:
                    if action == 0 or self.state[action - 1, brick_pos] == 1:
                        self.state[action, brick_pos] = 1
                    break

        # check if the game ends
        if self.state[-1].any():
            return self._add_moves_and_flatten(), 0, True, info

        # decrement the number of moves, change the state if they are 0
        #   and get a new set of moves
        self.available_moves -= 1
        if self.available_moves == 0:
            self._blow_wind()
            self.available_moves = np.random.randint(1, self.max_moves + 1)
            info['wind-has-blown'] = True

        # episode has not finished, return a reward of -1
        return self._add_moves_and_flatten(), -1, False, info

    def render(self, mode='human') -> None:
        """Renders the tower on the console."""
        for level in range(self.levels - 1, -1, -1):
            print(f'{level}: {len(self.state[level].nonzero()[0]) * "o"}')


if __name__ == '__main__':
    env = WindSweptEnv()
    _, done = env.reset(), False
    env.render()
    while not done:
        action = int(input('\nProvide the level to place the brick: '))
        _, _, done, _ = env.step(action)
        env.render()
