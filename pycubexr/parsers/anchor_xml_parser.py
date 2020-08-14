from typing import Dict, List
from xml.etree import ElementTree

from pycubexr import DEBUG
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
    if DEBUG:
        for cnode in result.cnodes:
            _assign_region(cnode, result)
    return result


def _bfs(root_list: List[CNode]):
    visited = {}
    queue = []
    ctr = 0
    for root_node in root_list:
        visited[root_node.id] = ctr
        ctr += 1
        queue.append(root_node)

    while queue:
        node = queue.pop(0)
        for child in node.get_children():
            if child.id not in visited:
                visited[child.id] = ctr
                ctr += 1
                queue.append(child)
    return visited


def _dfs(root_list: List[CNode]):
    visited = {}
    stack = []
    ctr = 0
    for root_node in reversed(root_list):
        stack.append(root_node)

    while stack:
        node = stack.pop()
        visited[node.id] = ctr
        ctr += 1
        for child in reversed(node.get_children()):
            stack.append(child)

    return visited


def _metric_tree_enumerations(result):
    dfs_enumeration = _dfs(result.cnodes)
    bfs_enumeration = _bfs(result.cnodes)
    for metric in result.metrics:
        if metric.metric_type == MetricType.EXCLUSIVE:
            metric.tree_enumeration = dfs_enumeration
        elif metric.metric_type == MetricType.INCLUSIVE:
            metric.tree_enumeration = bfs_enumeration


def _assign_region(cnode, result):
    cnode.region = [r for r in result.regions if r.id == cnode.callee_region_id][0]
    for c in cnode.get_children():
        _assign_region(c, result)
