import struct
from typing import List, BinaryIO, Any

from pycubexr.utils.metric_formats import METRIC_FORMATS

DATA_HEADER: bytes = b'CUBEX.DATA'


def parse_data(
        *,
        data_file: BinaryIO,
        # From the anchor.xml. NOT the Python struct data types, e.g., "i"
        data_type: str,
        # Either "<" or ">"
        endianness_format_char: str
) -> List[Any]:
    # Verify the data file header
    header = data_file.read(len(DATA_HEADER))
    assert header == DATA_HEADER

    raw = data_file.read()

    # Calculate the size for a single element
    single_value_size = struct.calcsize(METRIC_FORMATS[data_type])

    # Verify that the number of read bytes is divisible by the value size
    assert len(raw) % single_value_size == 0

    num_values = int(len(raw) / single_value_size)

    # Example: the format '<100i' means to parse/"unpack" 100 integers
    unpack_format = endianness_format_char + str(num_values) + METRIC_FORMATS[data_type]

    return list(struct.unpack(unpack_format, raw))
