import os

import gym
import pandas as pd
from gym import spaces
import numpy as np
import matplotlib.pyplot as plt

from yacht.data.datasets import TradingDataset
from yacht.environments.enums import Positions, Actions


class TradingEnv(gym.Env):
    def __init__(self, dataset: TradingDataset):
        self.seed()
        self.dataset = dataset
        self.window_size = dataset.window_size
        self.prices = dataset.get_prices()

        # spaces
        self.action_space = spaces.Discrete(len(Actions))
        self.observation_space_shape = (self.window_size, *self.dataset.get_item_shape())
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=self.observation_space_shape,
            dtype=np.float32
        )

        # episode
        self._start_tick = self.window_size - 1
        self._end_tick = len(self.prices) - 1
        self._done = None
        self._current_tick = None
        self._last_trade_tick = None
        self._position = None
        self._position_history = None
        self._total_reward = None
        self._total_profit = None
        self._first_rendering = None
        self.history = None

        self.reset()

    def set_dataset(self, dataset: TradingDataset):
        self.dataset = dataset
        self.prices = self.dataset.get_prices()

        # spaces
        self.observation_space_shape = (self.window_size, *self.dataset.get_item_shape())
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=self.observation_space_shape,
            dtype=np.float32
        )

        # episode
        self._end_tick = len(self.prices) - 1

    def reset(self):
        self._done = False
        self._current_tick = self._start_tick
        self._last_trade_tick = self._current_tick - 1
        self._position = Positions.Short
        self._position_history = ((self.window_size - 1) * [None]) + [self._position]
        self._total_reward = 0.
        self._total_profit = 1.  # unit
        self._first_rendering = True
        self.history = {}

        return self._get_observation()

    def step(self, action):
        self._done = False
        self._current_tick += 1

        if self._current_tick == self._end_tick:
            self._done = True

        step_reward = self.calculate_reward(action)
        self._total_reward += step_reward

        self.update_profit(action)

        trade = False
        if ((action == Actions.Buy.value and self._position == Positions.Short) or
                (action == Actions.Sell.value and self._position == Positions.Long)):
            trade = True

        if trade:
            self._position = self._position.opposite()
            self._last_trade_tick = self._current_tick

            self._position_history.append(self._position)
        else:
            self._position_history.append(None)

        observation = self._get_observation()
        info = dict(
            total_reward=self._total_reward,
            total_profit=self._total_profit,
            position=self._position.value
        )
        self._update_history(info)

        return observation, step_reward, self._done, info

    def _get_observation(self) -> np.array:
        observation = self.dataset[self._current_tick]

        return observation

    def _update_history(self, info):
        if not self.history:
            self.history = {key: [] for key in info.keys()}

        for key, value in info.items():
            self.history[key].append(value)

    def render(self, mode='human'):

        def _plot_position(position, tick):
            color = None
            if position == Positions.Short:
                color = 'red'
            elif position == Positions.Long:
                color = 'green'
            if color:
                plt.scatter(tick, self.prices[tick], color=color)

        if self._first_rendering:
            self._first_rendering = False
            plt.cla()
            plt.plot(self.prices)
            start_position = self._position_history[self._start_tick]
            _plot_position(start_position, self._start_tick)

        _plot_position(self._position, self._current_tick)

        plt.suptitle(
            "Total Reward: %.6f" % self._total_reward + ' ~ ' +
            "Total Profit: %.6f" % self._total_profit
        )

        plt.pause(0.01)

    def render_all(self):
        plt.plot(self.prices)

        position_ticks = pd.Series(index=self.prices.index)

        position_history = np.array(self._position_history)
        position_ticks[position_history == Positions.Short] = Positions.Short
        position_ticks[position_history == Positions.Long] = Positions.Long

        short_positions = position_ticks[position_ticks == Positions.Short]
        plt.plot(
            short_positions.index,
            self.prices.loc[short_positions.index],
            'rv',
            markersize=6
        )

        long_positions = position_ticks[position_ticks == Positions.Long]
        plt.plot(
            long_positions.index,
            self.prices.loc[long_positions.index],
            'g^',
            markersize=6
        )

        plt.suptitle(
            "Total Reward: %.6f" % self._total_reward + ' ~ ' +
            "Total Profit: %.6f" % self._total_profit
        )

    def close(self):
        plt.close()

    def save_rendering(self, name='trades.png'):
        plt.savefig(
            os.path.join(self.dataset.storage_dir, name)
        )

    def calculate_reward(self, action):
        raise NotImplementedError

    def update_profit(self, action):
        raise NotImplementedError

    def max_possible_profit(self):
        raise NotImplementedError()
