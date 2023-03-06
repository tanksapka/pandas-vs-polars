from enum import Enum
from pathlib import Path


class Constants(Enum):
    """
    Enum to store constant values.
    """
    sample_output_directory = Path(__file__).parent.parent.joinpath("sample_data")
    measurement_output_directory = Path(__file__).parent.parent.joinpath("result_data")
    # Chart related constants
    bar_width = 0.25
    ax2_offset = -0.25
    bottom_adjust = 0.30
