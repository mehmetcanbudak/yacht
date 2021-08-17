import datetime
import os
import sys
from abc import ABC, abstractmethod
from typing import Tuple, List, Optional, Dict

import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from stable_baselines3.common import results_plotter

from yacht import utils, Mode
from yacht.utils.wandb import WandBContext


class BaseRenderer(ABC):
    def __init__(self, data: pd.DataFrame):
        self.data = data

        self.fig = None
        self.ax = None

    def render(self, **kwargs):
        self._render(**kwargs)

    @abstractmethod
    def _render(self, **kwargs):
        pass


class MatPlotLibRenderer(BaseRenderer, ABC):
    def show(self):
        if self.fig:
            self.fig.show()

    def close(self):
        if self.fig:
            plt.close(self.fig)

    def save(self, file_path: str):
        if self.fig:
            self.fig.savefig(file_path)

            WandBContext.log_image_from(file_path)
        

class MplFinanceRenderer(BaseRenderer, ABC):
    def render(self, title: str, save_file_path: str, **kwargs):
        self._render(title, save_file_path, **kwargs)

        WandBContext.log_image_from(save_file_path)

    @abstractmethod
    def _render(self, title: str, save_file_path: str, **kwargs):
        pass


class KFoldRenderer(MatPlotLibRenderer):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)

        self.prices = self.data.loc[:, 'Close']

    def _render(self, **kwargs):
        train_indices: np.array = kwargs['train_indices']
        val_indices: np.array = kwargs['val_indices']

        self.fig, self.ax = plt.subplots()

        self.ax.plot(self.prices)
        self.ax.set_xticks(
            self.prices.index[
                np.linspace(0, self.prices.shape[0] - 1, 5).astype(np.int16)
            ])

        y_min = np.min(self.prices) * 0.9
        y_max = np.max(self.prices) * 1.1

        x_line_2_left = None
        x_line_2_right = None
        if np.max(val_indices) < np.min(train_indices):
            # Val split is in the left.
            x_line_1_left = self.prices.index[val_indices[-1]]
            x_line_1_right = self.prices.index[train_indices[0]]
        elif np.max(train_indices) < np.min(val_indices):
            # Val split is in the right.
            x_line_1_left = self.prices.index[train_indices[-1]]
            x_line_1_right = self.prices.index[val_indices[0]]
        else:
            # Val split is in the middle.
            diff = np.diff(train_indices)
            diff = np.concatenate([np.ones(shape=(1,)), diff])
            discontinuity_point = np.where(diff != 1)[0]
            assert len(discontinuity_point) == 1, 'There should be only one discontinuity point.'

            x_line_1_left = self.prices.index[train_indices[discontinuity_point - 1].item()]
            x_line_1_right = self.prices.index[val_indices[0]]
            x_line_2_left = self.prices.index[val_indices[-1]]
            x_line_2_right = self.prices.index[train_indices[discontinuity_point].item()]

        self.ax.text(
            x=self.prices.index[int(np.median(val_indices))],
            y=y_max + 10,
            s='Val'
        )
        self.ax.vlines(
            x_line_1_left,
            ymin=y_min,
            ymax=y_max,
            linestyles='dashed',
            colors='gray'
        )
        self.ax.vlines(
            x_line_1_right,
            ymin=y_min,
            ymax=y_max,
            linestyles='dashed',
            colors='gray'
        )
        if x_line_2_left and x_line_2_left:
            self.ax.vlines(
                x_line_2_left,
                ymin=y_min,
                ymax=y_max,
                linestyles='dashed',
                colors='gray'
            )
            self.ax.vlines(
                x_line_2_right,
                ymin=y_min,
                ymax=y_max,
                linestyles='dashed',
                colors='gray'
            )


class TrainTestSplitRenderer(MatPlotLibRenderer):
    def __init__(
            self,
            data: Dict[str, pd.DataFrame],
            train_interval: Tuple[datetime.datetime, datetime.datetime],
            test_interval: Tuple[datetime.datetime, datetime.datetime],
            rescale: bool = True
    ):
        super().__init__(data)

        assert len(train_interval) == 2 and len(test_interval) == 2
        assert train_interval[0] < train_interval[1] and test_interval[0] < test_interval[1]

        self.prices = self._get_prices(rescale)
        self.train_interval = train_interval
        self.test_interval = test_interval
        
    def _get_prices(self, rescale) -> Dict[str, pd.Series]:
        prices = dict()
        
        for ticker, values in self.data.items():
            if rescale:
                scaler = MinMaxScaler()

                indices = values.index
                values = values.loc[:, 'Close'].values.reshape(-1, 1)
                scaler.fit(values)

                values = scaler.transform(values)
                values = values.reshape(-1)
                prices[ticker] = pd.Series(index=indices, data=values)
            else:
                prices[ticker] = values.loc[:, 'Close']
                
        return prices

    def _render(self):
        self.fig, self.ax = plt.subplots()

        y_min = sys.float_info.max
        y_max = sys.float_info.min
        for ticker, prices in self.prices.items():
            self.ax.plot(prices, label=ticker)

            y_min = np.min(prices) if np.min(prices) < y_min else y_min
            y_max = np.max(prices) if np.max(prices) > y_max else y_max

        y_min *= 0.9
        y_max *= 1.1

        if self.train_interval[1] < self.test_interval[0]:
            x_line_left = self.train_interval[1]
            x_line_right = self.test_interval[0]
        else:
            x_line_left = self.test_interval[1]
            x_line_right = self.train_interval[0]

        start = min(self.train_interval[0], self.test_interval[0])
        end = max(self.train_interval[1], self.test_interval[1])
        self.ax.set_xticks([
            start,
            (x_line_left - start) / 2 + start,
            x_line_left,
            end
        ])

        self.ax.text(
            x=(self.train_interval[1] - self.train_interval[0]) / 2.5 + self.train_interval[0],
            y=y_max + 10,
            s='TrainVal Split'
        )
        self.ax.text(
            x=(self.test_interval[1] - self.test_interval[0]) / 2.5 + self.test_interval[0],
            y=y_max + 10,
            s='Test Split'
        )
        self.ax.vlines(
            x_line_left,
            ymin=y_min,
            ymax=y_max,
            linestyles='dashed',
            colors='gray'
        )
        self.ax.vlines(
            x_line_right,
            ymin=y_min,
            ymax=y_max,
            linestyles='dashed',
            colors='gray'
        )
        self.ax.legend()


class AssetEnvironmentRenderer(MplFinanceRenderer):
    def __init__(self, data: pd.DataFrame, start: datetime, end: datetime):
        super().__init__(data)

        self.start = start
        self.end = end

    def _render(self, title: str, save_file_path: str, **kwargs):
        tickers: List[str] = kwargs['tickers']
        actions = kwargs['actions']
        total_cash = kwargs.get('total_cash')
        total_units = kwargs.get('total_units')
        total_assets = kwargs.get('total_assets')

        if len(tickers) == 0:
            return

        # Trim missing values from the end.
        additional_plots = []
        dummy_data = None
        for ticker_idx, ticker in enumerate(tickers):
            ticker_actions = actions[:, ticker_idx]
            data = self.data.loc[(slice(None), ticker), ][:len(ticker_actions)]
            data = data.reset_index(level=1, drop=True)
            # Keep a reference only for the indices.
            dummy_data = data

            trading_renderer = TradingPositionRenderer(data)
            filename, file_extension = os.path.splitext(save_file_path)
            trading_renderer.render(
                title=f'{ticker}',
                save_file_path=f'{filename}_{ticker}{file_extension}',
                actions=ticker_actions
            )

            # Calculate actions.
            ticker_actions: pd.Series = pd.Series(index=data.index, data=ticker_actions)
            additional_plots.append(
                mpf.make_addplot(ticker_actions, panel=1, color='b', type='bar', width=1, ylabel='Actions'),
            )

            # Calculate units.
            ticker_units = total_units[:, ticker_idx]
            ticker_units: pd.Series = pd.Series(index=data.index, data=ticker_units)
            additional_plots.append(
                mpf.make_addplot(ticker_units, panel=2, color='b', type='bar', width=1, ylabel='Units'),
            )

        total_cash = pd.Series(index=dummy_data.index, data=total_cash)
        total_assets = pd.Series(index=dummy_data.index, data=total_assets)
        additional_plots.extend([
            mpf.make_addplot(total_cash, panel=3, color='b', type='bar', width=1, ylabel='Cash'),
            mpf.make_addplot(total_assets, panel=4, color='b', type='bar', width=1, ylabel='Assets')
        ])

        # TODO: See how to make panel y numbers not to overlap on the edges.
        mpf.plot(
            dummy_data,
            addplot=additional_plots,
            title=title,
            type='line',
            ylabel='Prices',
            panel_ratios=(1, 0.75, 0.75, 0.75, 0.75),
            figratio=(2, 1),
            figscale=1.5,
            savefig=save_file_path,
            volume=False
        )


class TradingPositionRenderer(MplFinanceRenderer):
    def _render(self, title: str, save_file_path: str, **kwargs):
        actions = kwargs['actions']
        positions = np.sign(actions)
        # first_item = positions[0].reshape(1)
        # positions = np.diff(positions, axis=0)
        # positions = np.concatenate([first_item, positions], axis=0)
        self.data = self.data.iloc[:len(positions)]

        # Calculate positions.
        positions = pd.Series(index=self.data.index, data=positions)

        short_positions_index = positions[positions < 0].index
        short_positions = positions.copy()
        short_positions[positions < 0] = self.data.loc[short_positions_index, 'High']
        short_positions[positions >= 0] = np.nan

        long_positions_index = positions[positions > 0].index
        long_positions = positions.copy()
        long_positions[positions > 0] = self.data.loc[long_positions_index, 'Low']
        long_positions[positions <= 0] = np.nan

        hold_position_index = positions[positions == 0].index
        hold_positions = positions.copy()
        hold_positions[positions == 0] = \
            (self.data.loc[hold_position_index, 'Low'] + self.data.loc[hold_position_index, 'High']) / 2
        hold_positions[positions < 0] = np.nan
        hold_positions[positions > 0] = np.nan

        additional_plots = []
        if len(short_positions[short_positions.notna()]) > 0:
            additional_plots.append(
                mpf.make_addplot(short_positions, type='scatter', markersize=25, marker='v', color='r')
            )
        if len(long_positions[long_positions.notna()]) > 0:
            additional_plots.append(
                mpf.make_addplot(long_positions, type='scatter', markersize=25, marker='^', color='g')
            )
        if len(hold_positions[hold_positions.notna()]) > 0:
            additional_plots.append(
                mpf.make_addplot(hold_positions, type='scatter', markersize=25, marker='.', color='y')
            )

        mpf.plot(
            self.data,
            addplot=additional_plots,
            title=title,
            type='line',
            ylabel='Prices',
            figratio=(2, 1),
            figscale=1.5,
            savefig=save_file_path,
            volume=True
        )


class RewardsRenderer(MatPlotLibRenderer):
    def __init__(self, total_timesteps: int, storage_dir: str, mode: Mode):
        super().__init__(None)

        self.total_timesteps = total_timesteps
        self.storage_dir = storage_dir
        self.mode = mode

    def _render(self):
        log_dir = utils.build_monitor_dir(self.storage_dir, mode=self.mode)
        results_plotter.plot_results(
            dirs=[log_dir],
            num_timesteps=self.total_timesteps,
            x_axis=results_plotter.X_TIMESTEPS,
            task_name=f'rewards_{self.mode.value}'
        )

    def show(self):
        super().show()

        plt.show()

    def close(self):
        super().close()

        plt.close()

    def save(self, file_path: str):
        super().save(file_path)

        plt.savefig(file_path)
        WandBContext.log_image_from(file_path)
