from enum import Enum
from pathlib import Path


class Constants(Enum):
    """
    Enum to store constant values.
    """
    output_directory = Path(__file__).parent.parent.joinpath("sample_data")
