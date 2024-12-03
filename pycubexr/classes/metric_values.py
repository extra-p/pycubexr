import logging
import warnings
from typing import List

import numpy as np

from pycubexr.classes import CNode, Metric
from pycubexr.classes.metric import MetricType
from pycubexr.classes.values import CubeValues
from pycubexr.utils.exceptions import InvalidConversionInstructionError


class MetricValues(object):

    def __init__(
            self,
            *,
            metric: Metric,
            cnode_indices: List[int],
            values: np.ndarray
    ):
        self.metric = metric
        self.values = values
        self.cnode_indices = {cid: i for i, cid in enumerate(cnode_indices)}
        self._num_locations = int(len(self.values) / len(self.cnode_indices))
        assert len(self.values) % len(self.cnode_indices) == 0

    def num_locations(self):
        return self._num_locations

    def cnode_values(self, cnode: CNode, convert_to_exclusive: bool = False, convert_to_inclusive: bool = False):
        if isinstance(cnode, int):
            warnings.warn('Calling with Cnode ID is deprecated use Cnode directly.', DeprecationWarning)
            if convert_to_inclusive or convert_to_exclusive:
                raise InvalidConversionInstructionError('Conversion is not supported when passing a Cnode ID.')
            cnode = CNode(_id=cnode, callee_region_id=-1)
        else:
            if convert_to_inclusive and convert_to_exclusive:
                raise InvalidConversionInstructionError()
            assert not (convert_to_inclusive and convert_to_exclusive)

        cid = cnode.id
        if cid not in self.cnode_indices:
            values = np.zeros(self.num_locations(), dtype=self.values.dtype)
        else:
            start_index = int(self.cnode_indices[cid] * self.num_locations())
            end_index = start_index + self.num_locations()
            values = self.values[start_index: end_index]  # creates no copy

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
    def _detect_negative_overflow(a, b):
        if np.issubdtype(a.dtype, np.unsignedinteger):
            check = a < b
            if np.any(check):
                b = b.copy()
                b[check] = a[check]
        elif np.issubdtype(a.dtype, np.signedinteger):
            pre_check = a > 0
            check = np.full_like(pre_check, False, dtype=bool)
            check[~pre_check] = -b[~pre_check] < np.iinfo(a.dtype).min - a[~pre_check]
            check[pre_check] |= -b[pre_check] > np.iinfo(a.dtype).max - a[pre_check]
            if np.any(check):
                if not np.issubdtype(a.dtype, np.int64):
                    bigger_type = np.min_scalar_type(int(np.iinfo(a.dtype).min) - 1)
                    b = b.astype(bigger_type, copy=False)
                else:
                    b = b.copy()
                    b[~pre_check & check] = -(np.iinfo(a.dtype).min - a[~pre_check & check])
                    b[pre_check & check] = -(np.iinfo(a.dtype).max - a[pre_check & check])
        return b

    def _convert_values(self, cnode: CNode, values: np.ndarray, to_inclusive: bool = True):
        # Go over all cnode children and add the metric values
        values = values.copy()
        for child_cnode in cnode.get_children():
            child_values = self.cnode_values(child_cnode,
                                             convert_to_inclusive=True,
                                             convert_to_exclusive=False)
            if to_inclusive:
                values += child_values
            else:
                if isinstance(values, np.ndarray) and np.issubdtype(values.dtype, np.integer):
                    child_values = self._detect_negative_overflow(values, child_values)
                values -= child_values
        return values

    def value(self, cnode: CNode, convert_to_exclusive: bool = False, convert_to_inclusive: bool = False):
        res = self.cnode_values(cnode, convert_to_exclusive, convert_to_inclusive)
        sum_ = res.sum()
        if isinstance(res, np.ndarray) and np.issubdtype(res.dtype, np.integer):
            if res.max() > np.iinfo(res.dtype).max // len(res):
                logging.info("Used overflow prevention for {0} of {1}".format(self.metric.name, cnode.region.name))
                # Overflow prevention, really slow
                sum_ = 0
                for r in res:
                    sum_ += int(r)

        if isinstance(sum_, CubeValues):
            return sum_.astype(float)
        else:
            return sum_

    def mean(self, cnode: CNode, convert_to_exclusive: bool = False, convert_to_inclusive: bool = False):
        res = self.cnode_values(cnode, convert_to_exclusive, convert_to_inclusive).mean()
        if isinstance(res, CubeValues):
            return res.astype(float)
        else:
            return res

    def __repr__(self):
        return 'MetricValues<{}>'.format(self.__dict__)
