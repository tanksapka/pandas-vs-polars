import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from pandas_vs_polars import Constants
from pathlib import Path
from typing import Optional


def parse_input(input_data: Optional[dict] = None, input_file: Optional[Path] = None) -> pd.DataFrame:
    if input_data is None and input_file is None:
        raise ValueError("Either input_data or input file has to be provided!")
    if input_data and input_file:
        raise ValueError("Only one argument should be provided!")

    if input_data:
        data = input_data
    if input_file:
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


def create_chart(df: pd.DataFrame, metric_column: str, metric_label: str, metric_magnitude: Optional[int] = 1,
                 chart_title: Optional[str] = None) -> Path:
    if chart_title is None:
        chart_title = metric_column.capitalize().replace("_", " ")

    fig, ax = plt.subplots()
    fig.set_size_inches(
        Constants.width_increment.value * df["group_by_column"].nunique() * df["sample_size"].nunique(),
        Constants.height.value
    )

    x_ticks, x_tick_labels, x_tick_len = list(), list(), 0
    for i, lib in enumerate(df["library_name"].unique()):
        tmp_df = df.loc[df["library_name"] == lib].sort_values(['group_by_column', 'sample_size'])
        ax.bar(x=np.arange(len(tmp_df.index)) + i * Constants.bar_width.value,
               height=tmp_df[metric_column] / metric_magnitude,
               width=Constants.bar_width.value, label=lib)
        x_ticks = np.arange(len(tmp_df.index)) + Constants.bar_width.value / 2
        x_tick_labels = tmp_df["sample_size"].apply(lambda x: f'{x / 1000000:,}m')
        x_tick_len = max(x_tick_len, max(x_tick_labels.apply(lambda x: len(x))))

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels)
    ax.tick_params('x', labelrotation=90.0)
    ax.set_ylabel(metric_label)
    ax.ticklabel_format(axis='y', useOffset=False, style='plain')
    ax.set_title(chart_title)
    ax.legend()
    ax.margins(Constants.x_margin.value, Constants.y_margin.value)

    ax2 = ax.twiny()
    ax2_pos = Constants.ax2_offset.value * (x_tick_len + 1)
    ax2.spines["bottom"].set_position(("axes", ax2_pos))
    ax2.tick_params('both', length=0, width=0, which='minor')
    ax2.tick_params('both', direction='in', which='major')
    ax2.xaxis.set_ticks_position("bottom")
    ax2.xaxis.set_label_position("bottom")

    ax2_ticks = [
        0, *(100 / df["group_by_column"].nunique() * i for i in range(1, df["group_by_column"].nunique())), 100
    ]

    ax2.set_xticks(ax2_ticks)
    ax2.xaxis.set_major_formatter(ticker.NullFormatter())
    ax2.xaxis.set_minor_locator(ticker.FixedLocator([i + (j - i) / 2 for i, j in zip(ax2_ticks, ax2_ticks[1:])]))
    ax2.xaxis.set_minor_formatter(ticker.FixedFormatter(df["group_by_column"].sort_values().unique()))
    ax2.grid(axis='x')
    fig.subplots_adjust(bottom=abs(ax2_pos))

    output_file = Constants.measurement_output_directory.value.joinpath(f'{metric_column}.png')
    plt.savefig(output_file)
    return output_file
