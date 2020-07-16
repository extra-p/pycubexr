from typing import List, Any

from pycubexr.classes import CNode, Metric
from pycubexr.classes.metric import MetricType
from pycubexr.utils.exceptions import InvalidConversionInstructionError


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

    def cnode_values(self, cnode: CNode, convert_to_exclusive: bool = False, convert_to_inclusive: bool = False):
        if convert_to_inclusive and convert_to_exclusive:
            raise InvalidConversionInstructionError()
        assert not (convert_to_inclusive and convert_to_exclusive)
        assert cnode.id in self.cnode_indices
        start_index = int(self.cnode_indices.index(cnode.id) * self.num_locations())
        end_index = start_index + self.num_locations()
        values = self.values[start_index:end_index]

        must_convert = ((convert_to_exclusive and self.metric.metric_type == MetricType.INCLUSIVE)
                        or (convert_to_inclusive and self.metric.metric_type == MetricType.EXCLUSIVE))
        if must_convert:
            values = self._convert_values(cnode, values, to_inclusive=convert_to_inclusive)
        # Copy the list instead of returning the values to prevent the user changing the internal values
        return [value for value in values]

    def location_value(self, cnode: CNode, location_id: int, convert_to_inclusive=False, convert_to_exclusive=False):
        assert location_id < self.num_locations()
        return self.cnode_values(
            cnode,
            convert_to_exclusive=convert_to_exclusive,
            convert_to_inclusive=convert_to_inclusive
        )[location_id]

    def _convert_values(self, cnode: CNode, values: List[Any], to_inclusive: bool = True):
        # Go over all cnode children and add the metric values
        # Does NOT change the values array!
        for child_cnode in cnode.get_all_children(with_self=False):
            if child_cnode.id not in self.cnode_indices:
                continue
            values = [
                x + y if to_inclusive else x - y
                for x, y
                in zip(values, self.cnode_values(
                    child_cnode,
                    convert_to_inclusive=False,
                    convert_to_exclusive=False)
                       )
            ]
        return values

    def __repr__(self):
        return 'MetricValues<{}>'.format(self.__dict__)
