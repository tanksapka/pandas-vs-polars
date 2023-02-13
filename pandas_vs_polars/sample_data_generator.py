from faker import Faker
from pathlib import Path


def generate_data(n: int, overwrite: bool) -> Path:
    """
    Generate one batch of sample data.

    :param n: number of rows to be generated
    :param overwrite: overwrite existing files or not
    :return: path of the sample file
    """
    fake = Faker()
    fields = (
        'username', 'ssn', 'name', 'date_of_birth', 'sex', 'mail', 'phone_number', 'post_code', 'city',
        'street_address', 'iban', 'job'
    )
    header = '\t'.join(fields)
    row_template = "\t".join(f"{{{field}}}" for field in fields)

    output_directory = Path(__file__).parent.parent.joinpath("sample_data")
    output_directory.mkdir(exist_ok=True)
    output_file = output_directory.joinpath(f'sample_{n}.csv')

    if not overwrite and output_file.exists():
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
    return output_file
