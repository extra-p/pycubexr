from typing import Dict, List
from xml.etree import ElementTree

from pycuber.classes import Metric, Region, CNode, SystemTreeNode
from pycuber.parsers import xml_parser_helper


class AnchorXMLParseResult(object):

    def __init__(
            self,
            *,
            attrs: Dict[str, str],
            metrics: List[Metric],
            regions: List[Region],
            cnodes: List[CNode],
            system_tree_nodes: List[SystemTreeNode]
    ):
        self.attrs = attrs
        self.metrics = metrics
        self.regions = regions
        self.cnodes = cnodes
        self.system_tree_nodes = system_tree_nodes


def parse_anchor_xml(root: ElementTree):
    result = AnchorXMLParseResult(
        attrs=xml_parser_helper.parse_attrs(root),
        metrics=xml_parser_helper.parse_metrics(root),
        regions=xml_parser_helper.parse_regions(root),
        cnodes=xml_parser_helper.parse_cnodes(root),
        system_tree_nodes=xml_parser_helper.parse_system_tree_nodes(root),
    )
    assert len(result.cnodes) == 1
    assert len(result.system_tree_nodes) == 1
    return result
