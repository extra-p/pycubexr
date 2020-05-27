from typing import List
from xml.etree import ElementTree

from cubex_lib.classes import Metric, Region, CNode, Location
from cubex_lib.parsers.xml_parser_helper import CubexXMLParsers


class CubexAnchorXMLParser(object):

    def __init__(self, root: ElementTree):
        self.attrs = CubexXMLParsers.parse_attrs(root)
        self.metrics = CubexXMLParsers.parse_metrics(root)
        self.regions = CubexXMLParsers.parse_regions(root)
        self.cnodes = CubexXMLParsers.parse_cnodes(root)
        self.system_tree_nodes = CubexXMLParsers.parse_system_tree_nodes(root)

    def get_metric_by_name(self, metric_name: str) -> Metric:
        return [metric for metric in self.metrics if metric.name == metric_name][0]

    def get_region(self, cnode: CNode) -> Region:
        return [region for region in self.regions if region.id == cnode.callee_region_id][0]

    def get_cnode(self, cnode_id: int) -> CNode:
        return [cnode for cnode in self.cnodes[0].get_all_children() if cnode.id == cnode_id][0]

    def get_locations(self) -> List[Location]:
        return self.system_tree_nodes[0].all_locations()
