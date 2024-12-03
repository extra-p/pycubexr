from typing import BinaryIO

from pycubexr.classes import MetricValues, Metric
from pycubexr.parsers.data_parser import parse_data
from pycubexr.parsers.index_parser import parse_index


def extract_metric_values(
        *,
        metric: Metric,
        index_file: BinaryIO,
        data_file: BinaryIO,
        allow_full_uint64_values: bool = False
) -> MetricValues:
    index = parse_index(index_file=index_file)
    values = parse_data(
        data_file=data_file,
        data_type=metric.data_type,
        endianness_format_char=index.endianness_format,
        allow_full_uint64_values=allow_full_uint64_values,
    )
    cnode_indices = [metric.tree_index_to_cid_map[tidx] for tidx in index.tree_indices]
    return MetricValues(
        metric=metric,
        cnode_indices=cnode_indices,
        values=values
    )
