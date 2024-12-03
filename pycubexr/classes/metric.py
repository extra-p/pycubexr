import warnings
from typing import List

from pycubexr.utils.metric_formats import METRIC_FORMATS


class MetricType(object):
    INCLUSIVE = 'INCLUSIVE'
    EXCLUSIVE = 'EXCLUSIVE'


class Metric(object):

    def __init__(
            self,
            *,
            name: str,
            _id: int,
            display_name: str,
            description: str,
            metric_type: str,
            data_type: str,
            units: str,
            url: str,
            childs: List
    ):
        assert hasattr(MetricType, metric_type)
        assert data_type in METRIC_FORMATS
        self.name = name
        self.id = _id
        self.display_name = display_name
        self.description = description
        self.metric_type = metric_type
        self.data_type = data_type
        self.units = units
        self.url = url
        self.tree_index_to_cid_map: dict = None
        self.childs = childs

    @property
    def tree_enumeration(self):
        warnings.warn('Accessing the tree enumeration is deprecated. Use cnode ids directly.', DeprecationWarning)
        if self.tree_index_to_cid_map is None:
            return None
        return {cid: tid for tid, cid in self.tree_index_to_cid_map.items()}

    def __repr__(self):
        return 'Metric<{}>'.format(self.__dict__)

    def get_all_children(self, with_self=True) -> List['Metric']:
        metrics = []
        if with_self:
            metrics.append(self)
        for child in self.childs:
            metrics += child.get_all_children()
        return metrics
