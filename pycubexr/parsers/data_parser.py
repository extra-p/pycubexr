import re
import struct
import zlib
from typing import List, BinaryIO, Any

from pycubexr.classes.values import convert_type
from pycubexr.utils.metric_formats import METRIC_FORMATS

DATA_HEADER: bytes = b'CUBEX.DATA'
ZDATA_HEADER: bytes = b'ZCUBEX.DATA'


def parse_data(
        *,
        data_file: BinaryIO,
        # From the anchor.xml. NOT the Python struct data types, e.g., "i"
        data_type: str,
        # Either "<" or ">"
        endianness_format_char: str,
        allow_full_uint64_values: bool = False
) -> List[Any]:
    # Verify the data file header
    header = data_file.read(len(DATA_HEADER))
    if header != DATA_HEADER:
        header = header + data_file.read(len(ZDATA_HEADER) - len(DATA_HEADER))
        assert header == ZDATA_HEADER
        raw = decompress_data(data_file, endianness_format_char)
    else:
        raw = data_file.read()

    data_type, parameters, metric_format = _get_metric_format(data_type)

    # Calculate the size for a single element
    single_value_size = struct.calcsize(metric_format)

    # Verify that the number of read bytes is divisible by the value size
    assert len(raw) % single_value_size == 0

    num_values = int(len(raw) / single_value_size)
    if len(metric_format) == 1:
        # Example: the format '<100i' means to parse/"unpack" 100 integers
        unpack_format = endianness_format_char + str(num_values) + metric_format
        data = struct.unpack(unpack_format, raw)
    else:
        unpack_format = endianness_format_char + metric_format
        data = struct.iter_unpack(unpack_format, raw)
    return convert_type(data_type, parameters, data, allow_full_uint64_values)


def _get_metric_format(data_type):
    parameters = None
    if '(' in data_type:
        # data type has parameters
        matches = re.fullmatch(r"^(.*?)\s*\(\s*(.*?)\s*\)\s*$", data_type)
        if matches is None:
            return None, None, None
        data_type = matches[1]
        if data_type not in METRIC_FORMATS:
            return None, None, None
        parameters = re.split(r"\s*,\s*", matches[2])
        try:
            metric_format = METRIC_FORMATS[data_type](*parameters)
        except ValueError:
            return None, None, None
    elif data_type not in METRIC_FORMATS:
        return None, None, None
    else:
        metric_format = METRIC_FORMATS[data_type]
    return data_type, parameters, metric_format


def decompress_data(data_file: BinaryIO, endianness_format_char: str):
    _sizeof_long_ = struct.calcsize('q')

    raw = data_file.read(_sizeof_long_)
    number_of_entries = struct.unpack(endianness_format_char + 'q', raw)[0]

    _num_infos_ = 3
    raw = data_file.read(_num_infos_ * number_of_entries * _sizeof_long_)
    raw_headers = struct.unpack(endianness_format_char + str(_num_infos_ * number_of_entries) + 'q', raw)
    entry_headers = (raw_headers[i:i + _num_infos_] for i in range(0, len(raw_headers), _num_infos_))

    decompressed = bytes()
    for uncompressed_pos, compressed_pos, compressed_size in entry_headers:
        if compressed_size == 0:
            continue

        raw = data_file.read(compressed_size)
        decompressed += zlib.decompress(raw)

    return decompressed
