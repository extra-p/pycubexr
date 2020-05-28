from typing import List
from xml.etree import ElementTree

from pycubex_parser.classes import Metric, Region, CNode, Location
from pycubex_parser.parsers import xml_parser_helper


class CubexAnchorXMLParser(object):

    def __init__(self, root: ElementTree):
        self.attrs = xml_parser_helper.parse_attrs(root)
        self.metrics = xml_parser_helper.parse_metrics(root)
        self.regions = xml_parser_helper.parse_regions(root)
        self.cnodes = xml_parser_helper.parse_cnodes(root)
        self.system_tree_nodes = xml_parser_helper.parse_system_tree_nodes(root)
        # TODO: is this always the case? All examples had this structure
        assert len(self.cnodes) == 1
        assert len(self.system_tree_nodes) == 1

    def get_metric_by_name(self, metric_name: str) -> Metric:
        return [metric for metric in self.metrics if metric.name == metric_name][0]

    def get_region(self, cnode: CNode) -> Region:
        return [region for region in self.regions if region.id == cnode.callee_region_id][0]

    def get_cnode(self, cnode_id: int) -> CNode:
        return [cnode for cnode in self.cnodes[0].get_all_children() if cnode.id == cnode_id][0]

    def get_locations(self) -> List[Location]:
        return self.system_tree_nodes[0].all_locations()

    def print_calltree(self, indent=0, cnode: CNode = None):
        if cnode is None:
            cnode = self.cnodes[0]

        print('\t' * indent, self.get_region(cnode).name)

        for child in cnode.get_children():
            self.print_calltree(indent + 1, cnode=child)
