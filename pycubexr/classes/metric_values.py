from typing import List, Any

from pycubexr.classes import CNode, Metric
from pycubexr.classes.metric import MetricType
from pycubexr.classes.values import BaseValue
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
        cid = self.metric.tree_enumeration[cnode.id]
        if cid not in self.cnode_indices:
            values = [0] * self.num_locations()
        else:
            start_index = int(self.cnode_indices.index(cid) * self.num_locations())
            end_index = start_index + self.num_locations()
            values = self.values[start_index: end_index]  # creates copy

        must_convert = ((convert_to_exclusive and self.metric.metric_type == MetricType.INCLUSIVE)
                        or (convert_to_inclusive and self.metric.metric_type == MetricType.EXCLUSIVE))
        if must_convert:
            values = self._convert_values(cnode, values, to_inclusive=convert_to_inclusive)
        return values

    def location_value(self, cnode: CNode, location_id: int, convert_to_inclusive=False, convert_to_exclusive=False):
        assert location_id < self.num_locations()
        return self.cnode_values(
            cnode,
            convert_to_exclusive=convert_to_exclusive,
            convert_to_inclusive=convert_to_inclusive
        )[location_id]

    @staticmethod
    def _iadd(a, b):
        assert len(a) == len(b)
        for i, y in enumerate(b):
            a[i] += y

    @staticmethod
    def _isub(a, b):
        assert len(a) == len(b)
        for i, y in enumerate(b):
            a[i] -= y

    def _convert_values(self, cnode: CNode, values: List[Any], to_inclusive: bool = True):
        # Go over all cnode children and add the metric values
        # Does change the values array!
        for child_cnode in cnode.get_children():
            child_values = self.cnode_values(child_cnode,
                                             convert_to_inclusive=True,
                                             convert_to_exclusive=False)
            if to_inclusive:
                self._iadd(values, child_values)
            else:
                self._isub(values, child_values)
        return values

    def value(self, cnode: CNode, convert_to_inclusive=False, convert_to_exclusive=False):
        res = sum(self.cnode_values(cnode, convert_to_inclusive, convert_to_exclusive))
        if isinstance(res, BaseValue):
            return res.try_convert()
        else:
            return res

    def mean(self, cnode: CNode, convert_to_inclusive=False, convert_to_exclusive=False):
        values = self.cnode_values(cnode, convert_to_inclusive, convert_to_exclusive)
        res = sum(values)
        if isinstance(res, BaseValue):
            res = res.try_convert()
        return res / len(values)

    def __repr__(self):
        return 'MetricValues<{}>'.format(self.__dict__)
