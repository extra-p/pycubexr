from typing import BinaryIO

from pycuber.classes import MetricValues, Metric
from pycuber.parsers.data_parser import parse_data
from pycuber.parsers.index_parser import parse_index


def extract_metric_values(
        *,
        metric: Metric,
        index_file: BinaryIO,
        data_file: BinaryIO
) -> MetricValues:
    index = parse_index(index_file=index_file)
    values = parse_data(
        data_file=data_file,
        data_type=metric.data_type,
        endianness_format_char=index.endianness_format
    )
    return MetricValues(
        cnode_indices=index.cnode_indices,
        values=values
    )
