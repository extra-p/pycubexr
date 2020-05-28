from typing import Dict, BinaryIO

from pycubex_parser.classes import MetricValues, Metric
from pycubex_parser.parsers.data_parser import CubexDataParser
from pycubex_parser.parsers.index_parser import CubexIndexParser


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

        index_parser = CubexIndexParser(
            index_file=index_file
        )
        data_parser = CubexDataParser(
            data_file=data_file,
            data_type=metric.data_type,
            endianness_format_char=index_parser.endianness_fmt
        )

        metric_values = MetricValues(
            cnode_indices=index_parser.cnode_indices,
            values=data_parser.parsed_values
        )
        self._metric_values[metric.id] = metric_values
        return metric_values
