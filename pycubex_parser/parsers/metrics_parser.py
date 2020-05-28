from typing import Dict, BinaryIO

from pycubex_parser.classes import MetricValues, Metric
from pycubex_parser.parsers.data_parser import parse_data
from pycubex_parser.parsers.index_parser import parse_index


class CubexMetricsParser(object):
    _metric_values: Dict[int, MetricValues]

    def __init__(self):
        self._metric_values = {}

    def get_metric_values(
            self,
            *,
            metric: Metric,
            index_file: BinaryIO,
            data_file: BinaryIO
    ) -> MetricValues:
        # TODO: memoization can lead to problems when different index_files/data_files for each metric are parsed.
        #  Why should this happen?
        if metric.id in self._metric_values:
            return self._metric_values[metric.id]

        index_parse_result = parse_index(
            index_file=index_file
        )

        values = parse_data(
            data_file=data_file,
            data_type=metric.data_type,
            endianness_format_char=index_parse_result.endianness_format
        )

        metric_values = MetricValues(
            cnode_indices=index_parse_result.cnode_indices,
            values=values
        )
        self._metric_values[metric.id] = metric_values
        return metric_values
