import struct
from typing import List, BinaryIO, Any

from cubex_lib.utils.metric_formats import METRIC_FORMATS


class DataParser(object):
    parsed_values: List[Any]
    HEADER: bytes = b'CUBEX.DATA'

    def __init__(
            self,
            *,
            data_file: BinaryIO,
            data_type: str,
            # Either "<" or ">"
            endianness_format_char: str,
            num_locations: int,
            num_cnodes: int
    ):
        # Verify the data file header
        header = data_file.read(len(self.HEADER))
        assert header == self.HEADER

        # Calculate how many values the data file should contain
        values_to_parse = num_locations * num_cnodes

        # Example: the format '<100i' means to parse/"unpack" 100 integers
        unpack_format = endianness_format_char + str(values_to_parse) + METRIC_FORMATS[data_type]

        # Calculate how many bytes the file SHOULD have
        value_size = struct.calcsize(unpack_format)

        # Read the whole data file
        raw = data_file.read()

        assert len(raw) == value_size

        self.parsed_values = list(struct.unpack(unpack_format, raw))
        assert len(self.parsed_values) == values_to_parse
