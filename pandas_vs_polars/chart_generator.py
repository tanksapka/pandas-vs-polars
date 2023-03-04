import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from enum import Enum
from pathlib import Path
from typing import Optional


class Constants(Enum):
    bar_width = 0.25
    ax2_offset = -0.25
    bottom_adjust = 0.30


def parse_input(input_file: Path) -> pd.DataFrame:
    with input_file.open() as fh:
        data = json.load(fh)

    tab_data = list()
    for k, v in data.items():
        for t, s in v.items():
            for sk, sv in s.items():
                tab_data.append([k, t, sk, sv["memory_current"], sv["memory_peak"], sv["execution_time"]])

    col_names = ["file_name", "library_name", "group_by_column", "memory_current", "memory_peak", "execution_time"]
    df = pd.DataFrame(data=tab_data, columns=col_names)
    df.insert(1, 'sample_size', df.file_name.apply(lambda x: int(x.replace("sample_", "").replace(".csv", ""))))
    return df


def create_chart(df: pd.DataFrame, metric_column: str, metric_label: str, metric_magnitude: Optional[int] = 1):
    # TODO: Add chart title as well
    # TODO: Return saved image file's path
    fig, ax = plt.subplots()

    x_ticks, x_tick_labels = list(), list()
    for i, lib in enumerate(df["library_name"].unique()):
        tmp_df = df.loc[df["library_name"] == lib].sort_values(['group_by_column', 'sample_size'])
        ax.bar(x=np.arange(len(tmp_df.index)) + i * Constants.bar_width.value,
               height=tmp_df[metric_column] / metric_magnitude,
               width=Constants.bar_width.value, label=lib)
        x_ticks = np.arange(len(tmp_df.index)) + Constants.bar_width.value / 2
        x_tick_labels = tmp_df["sample_size"].apply(lambda x: f'{x / 1000000:,}m')

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels)
    ax.tick_params('x', labelrotation=90.0)
    ax.set_ylabel(metric_label)
    ax.ticklabel_format(axis='y', useOffset=False, style='plain')
    ax.legend()

    ax2 = ax.twiny()
    ax2.spines["bottom"].set_position(("axes", Constants.ax2_offset.value))  # TODO: make distance dynamic based on sample size
    ax2.tick_params('both', length=0, width=0, which='minor')
    ax2.tick_params('both', direction='in', which='major')
    ax2.xaxis.set_ticks_position("bottom")
    ax2.xaxis.set_label_position("bottom")

    ax2_ticks = [0, *((df["sample_size"].nunique() * i) + 0.5 for i in range(1, df["group_by_column"].nunique() + 1))]
    ax2_ticks[-1] = ax2_ticks[-1] + 0.5

    ax2.set_xticks(ax2_ticks)
    ax2.xaxis.set_major_formatter(ticker.NullFormatter())
    ax2.xaxis.set_minor_locator(ticker.FixedLocator([i + (j - i) / 2 for i, j in zip(ax2_ticks, ax2_ticks[1:])]))
    ax2.xaxis.set_minor_formatter(ticker.FixedFormatter(df["group_by_column"].sort_values().unique()))
    ax2.grid(axis='x')
    fig.subplots_adjust(bottom=Constants.bottom_adjust.value)  # TODO: make distance dynamic based on sample size

    plt.savefig('tst.png')
    # plt.show()


if __name__ == '__main__':
    p = Path(__file__).resolve().parent.parent.joinpath('results.json')
    d = parse_input(p)
    create_chart(d, 'execution_time', 'million nanoseconds', 1000000)
