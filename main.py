import argparse
import json
import logging
import toml
from collections import defaultdict
from logging import config
from pandas_vs_polars import Constants
from pandas_vs_polars.bm_group_by import pandas_group_by, polars_group_by
from pandas_vs_polars.chart_generator import parse_input, create_chart
from pandas_vs_polars.sample_data_generator import generate_data_wrapper
from pathlib import Path

log_cfg = toml.load(Path(__file__).parent.joinpath('pyproject.toml'))
config.dictConfig(log_cfg)
_logger = logging.getLogger(__name__)


def main() -> None:
    """
    Gathers user input and runs performance tests and collects statistics.
    """
    parser = argparse.ArgumentParser(
        description="Pandas vs Polars performance tester. The program creates sample data and runs various tests "
                    "with both packages. After running these tests collects memory usage and execution time statistics "
                    "as well."
    )
    parser.add_argument(
        "-n", type=int, required=False, default=1000000, help="Maximum number of rows in the last batch"
    )
    parser.add_argument(
        "-o", "--overwrite", action=argparse.BooleanOptionalAction, required=False, default=False,
        help="Force to regenerate sample data and overwrite existing files. Upon rerunning with higher count it "
             "generates only the delta files."
    )
    parser.add_argument(
        "-c", "--clean", action=argparse.BooleanOptionalAction, required=False, default=False,
        help="Clean up sample data once done"
    )
    args = parser.parse_args()
    _logger.info(args)
    paths = generate_data_wrapper(args.n, args.overwrite)

    _logger.info("Doing benchmarking on group by")
    results = defaultdict(dict)
    for path in paths:
        results[path.name]["pandas"] = pandas_group_by(path)
        results[path.name]["polars"] = polars_group_by(path)

    Constants.measurement_output_directory.value.mkdir(parents=True, exist_ok=True)
    result_file = Constants.measurement_output_directory.value.joinpath("results.json")
    _logger.info(f"Saving results to file: {result_file}")
    with result_file.open("w") as fh:
        json.dump(results, fh, indent=2)

    _logger.info("Generating charts from results")
    create_chart(parse_input(input_data=results), 'execution_time', 'million nanoseconds', 1000000)
    create_chart(parse_input(input_data=results), 'memory_peak', 'megabytes', 1024*1024)

    if args.clean:
        _logger.info("Cleaning up sample files")
        for path in paths:
            _logger.info(f"Deleting file {path}")
            path.unlink()


if __name__ == "__main__":
    main()
