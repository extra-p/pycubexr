from typing import List, Any

from cubex_lib.classes import Metric


class MetricValues(object):

    def __init__(
            self,
            *,
            metric: Metric,
            cnode_indices: List[int],
            # The first dimension is the cnode, the second the location (= thread)
            values: List[Any]
    ):
        self.metric = metric
        self.cnode_indices = cnode_indices
        self.values = values

    def __repr__(self):
        return 'MetricValues<{}>'.format(self.__dict__)
