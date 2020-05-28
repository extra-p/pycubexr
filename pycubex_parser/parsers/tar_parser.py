import tarfile
from typing import List
from xml.etree import ElementTree

from pycubex_parser.classes import Metric, MetricValues
from pycubex_parser.parsers.anchor_xml_parser import CubexAnchorXMLParser
from pycubex_parser.parsers.metrics_parser import CubexMetricsParser
from pycubex_parser.utils.exceptions import MissingMetricError


class CubexTarParser(object):
    metrics_parser: CubexMetricsParser
    anchor_parser: CubexAnchorXMLParser

    def __init__(self, cubex_filename: str):
        self.cubex_filename = cubex_filename

    def __enter__(self):
        self.cubex_file = tarfile.open(self.cubex_filename)

        with self.cubex_file.extractfile('anchor.xml') as anchor_file:
            anchor = ElementTree.parse(anchor_file)

        self.anchor_parser = CubexAnchorXMLParser(anchor)
        self.metrics_parser = CubexMetricsParser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cubex_file.close()

    def get_metric_values(
            self,
            metric: Metric
    ) -> MetricValues:
        index_file_name = f'{metric.id}.index'
        data_file_name = f'{metric.id}.data'

        if index_file_name not in self._tar_file_members():
            raise MissingMetricError(metric)

        with self.cubex_file.extractfile(index_file_name) as index_file, \
                self.cubex_file.extractfile(data_file_name) as data_file:
            metric_values = self.metrics_parser.get_metric_values(
                metric=metric,
                index_file=index_file,
                data_file=data_file
            )
            assert metric_values.num_locations() == len(self.anchor_parser.get_locations())
            return metric_values

    def _tar_file_members(self) -> List[str]:
        return [x.name for x in self.cubex_file.getmembers()]