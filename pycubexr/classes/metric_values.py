from typing import List, Any


class MetricValues(object):

    def __init__(
            self,
            *,
            cnode_indices: List[int],
            values: List[Any]
    ):
        self.values = values
        self.cnode_indices = cnode_indices
        assert len(self.values) % len(self.cnode_indices) == 0

    def num_locations(self):
        return int(len(self.values) / len(self.cnode_indices))

    def cnode_values(self, cnode_id: int):
        assert cnode_id in self.cnode_indices
        start_index = int(self.cnode_indices.index(cnode_id) * self.num_locations())
        end_index = start_index + self.num_locations()
        return self.values[start_index:end_index]

    def location_value(self, cnode_id: int, location_id: int):
        assert location_id < self.num_locations()
        return self.cnode_values(cnode_id)[location_id]

    def __repr__(self):
        return 'MetricValues<{}>'.format(self.__dict__)
