import tarfile
from gzip import GzipFile
from os import PathLike
from tarfile import TarFile
from typing import List, Dict, Tuple, Union
from xml.etree import ElementTree

from pycubexr.classes import Metric, MetricValues, Region, CNode, Location
from pycubexr.parsers.anchor_xml_parser import parse_anchor_xml, AnchorXMLParseResult
from pycubexr.parsers.metrics_parser import extract_metric_values
from pycubexr.utils.caching import cached_property
from pycubexr.utils.custom_tarinfo import TarInfoWithoutCheck
from pycubexr.utils.exceptions import MissingMetricError


class CubexParser(object):
    _cubex_file: TarFile
    _cubex_filename: Union[str, PathLike]
    _anchor_result: AnchorXMLParseResult
    _metric_values: Dict[Tuple[int, bool], MetricValues]

    def __init__(self, cubex_filename: Union[str, PathLike]):
        self._cubex_filename = cubex_filename
        self._metric_values = {}

    def __enter__(self):
        try:
            self._cubex_file = tarfile.open(self._cubex_filename)
        except tarfile.ReadError:
            self._cubex_file = tarfile.open(self._cubex_filename, tarinfo=TarInfoWithoutCheck)

        self._tar_file_member_list = [x.name for x in self._cubex_file.getmembers()]

        with self._cubex_file.extractfile('anchor.xml') as anchor_file:
            xml_header = anchor_file.read(5)
            anchor_file.seek(0, 0)
            if xml_header != b"<?xml":
                # if not starting with xml assume compressed
                with GzipFile(fileobj=anchor_file) as compressed_anchor:
                    anchor = ElementTree.parse(compressed_anchor)
                    self._anchor_result = parse_anchor_xml(anchor)
            else:
                anchor = ElementTree.parse(anchor_file)
                self._anchor_result = parse_anchor_xml(anchor)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._metric_values.clear()
        self._cubex_file.close()

    def get_metric_values(
            self,
            metric: Metric,
            cache: bool = True, *,
            allow_full_uint64_values: bool = False
    ) -> MetricValues:
        """
        Retrieves the values for the specified metric.
        :param metric: The specified metric
        :param cache: Enables caching of the values to accelerate future accesses.
        :param allow_full_uint64_values: Enables the usage of UINT64 values greater than 0xFFFF_FFFF_FFFF_FBFF.
            Disabled by default to match the CubeLib behavior.
        :return: The measured values for the specified metric.
        """
        if (metric.id, allow_full_uint64_values) in self._metric_values:
            return self._metric_values[metric.id, allow_full_uint64_values]

        index_file_name = '{}.index'.format(metric.id)
        data_file_name = '{}.data'.format(metric.id)

        if index_file_name not in self._tar_file_members():
            raise MissingMetricError(metric)

        with self._cubex_file.extractfile(index_file_name) as index_file, \
                self._cubex_file.extractfile(data_file_name) as data_file:
            metric_values = extract_metric_values(
                metric=metric,
                index_file=index_file,
                data_file=data_file,
                allow_full_uint64_values=allow_full_uint64_values
            )

            assert metric_values.num_locations() == self._num_locations
            if cache:
                self._metric_values[metric.id, allow_full_uint64_values] = metric_values
            return metric_values

    @cached_property
    def _num_locations(self):
        return len(self.get_locations())

    def get_metrics(self):
        return self._anchor_result.metrics

    @cached_property
    def _metrics_dict(self):
        metrics = {}

        def walk_tree(childs):
            for metric in childs:
                metrics[metric.name] = metric
                walk_tree(metric.childs)

        walk_tree(self._anchor_result.metrics)
        return metrics

    def all_metrics(self):
        return list(self._metrics_dict.values())

    def get_metric_by_name(self, metric_name: str) -> Metric:
        return self._metrics_dict[metric_name]

    def get_region(self, cnode: CNode) -> Region:
        return self._anchor_result.regions_by_id[cnode.callee_region_id]

    def get_cnode(self, cnode_id: int) -> CNode:
        return self._anchor_result.all_cnodes.get(cnode_id)

    def get_root_cnodes(self) -> List[CNode]:
        return self._anchor_result.cnodes

    def get_region_by_name(self, name: str):
        return [region for region in self._anchor_result.regions if region.name == name][0]

    def all_cnodes(self) -> List[CNode]:
        return list(self._anchor_result.all_cnodes.values())

    def get_cnodes_for_region(self, region_id: int):
        return [cnode for cnode in self.all_cnodes() if cnode.callee_region_id == region_id]

    def get_locations(self) -> List[Location]:
        return self._anchor_result.system_tree_nodes[0].all_locations()

    def get_calltree(self, indent=0, cnode: CNode = None):
        if cnode is None:
            cnode = self._anchor_result.cnodes[0]
        call_tree_string = ""
        child_string = ""
        child_string += "-" * indent + self.get_region(cnode).name
        call_tree_string += child_string
        call_tree_string += "\n"

        for child in cnode.get_children():
            tmp = self.get_calltree(indent + 1, cnode=child)
            if tmp is not None:
                call_tree_string += tmp

        return call_tree_string

    def print_calltree(self, indent=0, cnode: CNode = None):
        if cnode is None:
            cnode = self._anchor_result.cnodes[0]

        print('\t' * indent, self.get_region(cnode).name)

        for child in cnode.get_children():
            self.print_calltree(indent + 1, cnode=child)

    def _tar_file_members(self) -> List[str]:
        return self._tar_file_member_list
