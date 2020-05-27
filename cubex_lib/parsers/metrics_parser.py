from typing import Dict, BinaryIO

from cubex_lib.classes import MetricValues, Metric
from cubex_lib.parsers.anchor_xml_parser import CubexAnchorXMLParser
from cubex_lib.parsers.data_parser import CubexDataParser
from cubex_lib.parsers.index_parser import CubexIndexParser


class CubexMetricsParser(object):
    _metric_values: Dict[int, MetricValues]

    def __init__(
            self,
            # TODO: this SHOULD not be passed
            anchor_parser: CubexAnchorXMLParser
    ):
        self._metric_values = {}
        self._anchor_parser = anchor_parser

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
