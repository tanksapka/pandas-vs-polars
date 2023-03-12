import logging
from faker import Faker
from pandas_vs_polars import Constants
from pandas_vs_polars.utils import generate_next_n, time_it
from pathlib import Path

_logger = logging.getLogger(__name__)


@time_it
def generate_data(n: int, overwrite: bool) -> Path:
    """
    Generate one batch of sample data.

    :param n: number of rows to be generated
    :param overwrite: overwrite existing files or not
    :return: path of the sample file
    """
    _logger.info(f"Generating sample data of size {n:,}")
    fake = Faker()
    fields = (
        'username', 'ssn', 'name', 'date_of_birth', 'sex', 'mail', 'phone_number', 'post_code', 'city',
        'street_address', 'iban', 'job'
    )
    header = '\t'.join(fields)
    row_template = "\t".join(f"{{{field}}}" for field in fields)

    Constants.sample_output_directory.value.mkdir(exist_ok=True)
    output_file = Constants.sample_output_directory.value.joinpath(f'sample_{n}.csv')

    if not overwrite and output_file.exists():
        _logger.info(f"Output file {output_file} already exists, overwrite {overwrite}")
        return output_file

    with output_file.open("w") as fh:
        fh.write(f"{header}\n")
        for _ in range(n):
            basic_data: dict = fake.profile()
            basic_data.pop('residence')
            basic_data.pop('address')
            basic_data.update({
                'date_of_birth': fake.date_of_birth(),
                'phone_number': fake.phone_number(),
                'post_code': fake.postcode(),
                'city': fake.city(),
                'street_address': fake.street_address(),
                'iban': fake.iban(),
            })
            fh.write(f'{row_template.format(**basic_data)}\n')
    _logger.info(f"Generating finished, file saved: {output_file}")
    return output_file


def generate_data_wrapper(n: int, overwrite: bool) -> list[Path]:
    """
    Wrapper function to handle sample data generation.

    :param n: number of rows to be generated
    :param overwrite: overwrite existing files or not
    :return: list of path of the sample file
    """
    paths = list()
    for batch in generate_next_n():
        if batch > n:
            break
        paths.append(generate_data(batch, overwrite))
    return paths
