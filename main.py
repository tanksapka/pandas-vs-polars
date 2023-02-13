import argparse


def main() -> None:
    """
    Gathers user input and runs performance tests and collects statistics.
    """
    parser = argparse.ArgumentParser(
        description="Pandas vs Polars performance tester. The program creates sample data and runs various test "
                    "with both packages. After running collects memory usage and execution time statistics as well."
    )
    parser.add_argument(
        "-n", type=int, required=False, default=1000000, help="Maximum number of rows in the last batch"
    )
    parser.add_argument(
        "-o", "--overwrite", type=bool, required=False, default=False,
        help="Force to regenerate sample data and overwrite existing files. Upon rerunning with higher count it "
             "generates only the delta files."
    )
    parser.add_argument(
        "-c", "--clean", type=bool, required=False, default=False, help="Clean up sample data once done"
    )
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
