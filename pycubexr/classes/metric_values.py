from typing import List, Any

from pycubexr.classes import CNode, Metric
from pycubexr.classes.metric import MetricType


class MetricValues(object):

    def __init__(
            self,
            *,
            metric: Metric,
            cnode_indices: List[int],
            values: List[Any]
    ):
        self.metric = metric
        self.values = values
        self.cnode_indices = cnode_indices
        assert len(self.values) % len(self.cnode_indices) == 0

    def num_locations(self):
        return int(len(self.values) / len(self.cnode_indices))

    def cnode_values(self, cnode: CNode, convert_to_exclusive: bool = True, convert_to_inclusive: bool = False):
        assert cnode.id in self.cnode_indices
        start_index = int(self.cnode_indices.index(cnode.id) * self.num_locations())
        end_index = start_index + self.num_locations()
        values = self.values[start_index:end_index]
        if convert_to_exclusive and self.metric.metric_type == MetricType.EXCLUSIVE:
            values = self._calculate_exclusive(cnode, values)
        # Copy the list instead of returning the values to prevent the user changing the internal values
        return [value for value in values]

    def location_value(self, cnode: CNode, location_id: int):
        assert location_id < self.num_locations()
        return self.cnode_values(cnode)[location_id]

    def _calculate_exclusive(self, cnode: CNode, values: List[Any]):
        # Go over all cnode children and add the metric values
        # Does NOT change the values array!
        for child_cnode in cnode.get_all_children(with_self=False):
            if child_cnode.id not in self.cnode_indices:
                continue
            values = [
                x + y
                for x, y
                in zip(values, self.cnode_values(child_cnode, convert_to_exclusive=False))
            ]
        return values

    def __repr__(self):
        return 'MetricValues<{}>'.format(self.__dict__)
