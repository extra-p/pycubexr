from typing import List, Any, Optional

from cubex_lib.classes import CNode


class MetricValues(object):
    cnodes: Optional[List[CNode]]
    cnode_values: Optional[List[List[Any]]]

    def __init__(
            self,
            *,
            # A list of cnode indexes where cnode_indices[10] == 1 means that
            # cnode_values[10] contains the metric values for the cnode with id == 1
            cnode_indices: List[int],
            # The first dimension is the cnode, the second the location (= thread)
            values: List[Any],
            # These are the cnode_indices resolved to CNode instances
            cnodes: List[CNode] = None,
            # An 2-d array where
            # - the first dimension is the cnode index (cnode_indices) and
            # - the second is the location index (= threads)
            cnode_values: List[List[Any]] = None
    ):
        self.values = values
        self.cnodes = cnodes
        self.cnode_values = cnode_values
        self.cnode_indices = cnode_indices

    def __repr__(self):
        return 'MetricValues<{}>'.format(self.__dict__)
