from typing import Dict, List
from xml.etree import ElementTree

from pycubexr.classes import Metric, Region, CNode, SystemTreeNode
from pycubexr.classes.metric import MetricType
from pycubexr.parsers import xml_parser_helper


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
        self.regions_by_id = {r.id: r for r in regions}
        self.all_cnodes = {cnode.id: cnode for root_cnode in cnodes for cnode in root_cnode.get_all_children()}


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

    _metric_tree_enumerations(result)
    for cnode in result.all_cnodes.values():
        cnode.region = result.regions_by_id[cnode.callee_region_id]
    return result


def _wide_enumeration(root_list: List[CNode]):
    # does not implement breadth first search
    visited = {}
    stack = []
    ctr = 0

    for root_node in root_list:
        visited[ctr] = root_node.id
        ctr += 1
        stack.append(root_node)
        while stack:
            node = stack.pop()
            for child in node.get_children():
                visited[ctr] = child.id
                ctr += 1
            for child in reversed(node.get_children()):
                stack.append(child)
    return visited


def _deep_enumeration(root_list: List[CNode]):
    visited = {}
    stack = []
    ctr = 0
    for root_node in reversed(root_list):
        stack.append(root_node)

    while stack:
        node = stack.pop()
        visited[ctr] = node.id
        ctr += 1
        for child in reversed(node.get_children()):
            stack.append(child)

    return visited


def _metric_tree_enumerations(result):
    deep_enumeration = _deep_enumeration(result.cnodes)
    wide_enumeration = _wide_enumeration(result.cnodes)

    def walk_tree(childs):
        for metric in childs:
            if metric.metric_type == MetricType.EXCLUSIVE:
                metric.tree_index_to_cid_map = deep_enumeration
            elif metric.metric_type == MetricType.INCLUSIVE:
                metric.tree_index_to_cid_map = wide_enumeration
            walk_tree(metric.childs)

    walk_tree(result.metrics)


def _assign_region(cnode, result):
    cnode.region = [r for r in result.regions if r.id == cnode.callee_region_id][0]
    for c in cnode.get_children():
        _assign_region(c, result)
