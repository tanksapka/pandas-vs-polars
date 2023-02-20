"""
Benchmarking method for group by:
 1. On column sex
 2. On column post_code
 3. On column city
 4. On columns city and post code
 5. On column job
 6. On year(date_of_birth)
Do username count as aggregating function
"""
import logging
import pandas as pd
import polars as pl
import time
import tracemalloc
from pandas_vs_polars.utils import time_it
from pathlib import Path


_logger = logging.getLogger(__name__)

columns = (
    ['sex'],
    ['post_code'],
    ['city'],
    ['city', 'post_code'],
    ['job'],
    # ['year_dob'],
)
# TODO: city and post_code are way too unique, add year for date of birth


@time_it
def pandas_group_by(file_path: Path):
    tracemalloc.start()
    _logger.info(f"[pandas] running group by on file {file_path.name}")
    df = pd.read_csv(file_path, sep="\t")
    mem_curr, mem_peak = tracemalloc.get_traced_memory()
    _logger.info(f"[pandas] memory usage current: {mem_curr:,}, peak: {mem_peak:,}")
    _logger.info(f"[pandas] dataframe shape {df.shape}")
    for col in columns:
        _logger.info(f"[pandas] group by on {col}")
        tic = time.perf_counter_ns()
        result = df[['username', *col]].groupby(by=col, as_index=False).count()
        toc = time.perf_counter_ns() - tic
        mem_curr, mem_peak = tracemalloc.get_traced_memory()
        _logger.info(f"[pandas] memory usage current: {mem_curr:,}, peak: {mem_peak:,}")
        _logger.info(f"[pandas] group by took {toc:,} ns, shape {result.shape}")
    tracemalloc.stop()


@time_it
def polars_group_by(file_path: Path) -> None:
    tracemalloc.start()
    _logger.info(f"[polars] running group by on file {file_path.name}")
    for col in columns:
        _logger.info(f"[polars] group by on {col}")
        tic = time.perf_counter_ns()
        result = pl.scan_csv(file_path, sep="\t").groupby(col).agg(pl.count().alias('username')).collect()
        toc = time.perf_counter_ns() - tic
        mem_curr, mem_peak = tracemalloc.get_traced_memory()
        _logger.info(f"[polars] memory usage current: {mem_curr:,}, peak: {mem_peak:,}")
        _logger.info(f"[polars] group by took {toc:,} ns, shape {result.shape}")
    tracemalloc.stop()
