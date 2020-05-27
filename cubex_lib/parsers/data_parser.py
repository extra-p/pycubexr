import struct
from typing import List, BinaryIO, Any

from cubex_lib.utils.metric_formats import METRIC_FORMATS


class CubexDataParser(object):
    parsed_values: List[Any]
    HEADER: bytes = b'CUBEX.DATA'

    def __init__(
            self,
            *,
            data_file: BinaryIO,
            data_type: str,
            # Either "<" or ">"
            endianness_format_char: str
    ):
        # Verify the data file header
        header = data_file.read(len(self.HEADER))
        assert header == self.HEADER

        raw = data_file.read()

        # Calculate the size for a single element
        single_value_size = struct.calcsize(METRIC_FORMATS[data_type])

        # Verify that the number of read bytes is divisible by the value size
        assert len(raw) % single_value_size == 0

        num_values = int(len(raw) / single_value_size)

        # Example: the format '<100i' means to parse/"unpack" 100 integers
        unpack_format = endianness_format_char + str(num_values) + METRIC_FORMATS[data_type]
        self.parsed_values = list(struct.unpack(unpack_format, raw))
