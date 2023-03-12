from enum import Enum
from pathlib import Path


class Constants(Enum):
    """
    Enum to store constant values.
    """
    sample_output_directory = Path(__file__).parent.parent.joinpath("sample_data")
    measurement_output_directory = Path(__file__).parent.parent.joinpath("result_data")
    # Chart related constants
    width = 6.4
    width_increment = 0.4
    height = 4.8
    x_margin = 0
    y_margin = 0.05
    bar_width = 0.25
    ax2_offset = -0.04
