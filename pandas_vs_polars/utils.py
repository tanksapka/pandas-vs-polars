import logging
import time
from functools import wraps
from itertools import cycle
from typing import Iterator

_logger = logging.getLogger(__name__)


def time_it(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        delta = time.perf_counter() - start
        _logger.info(f'{fn.__name__} took: {delta:.6f} seconds')
        return result

    return wrapper


def generate_next_n() -> Iterator[int]:
    """
    Generator to provide next batch number. Starts at 1 000 and keeps multiplying with 5 and 2 (1k, 5k, 10k...)

    :return: next batch number
    """
    n = 1000
    for m in cycle((5, 2)):
        yield n
        n *= m
