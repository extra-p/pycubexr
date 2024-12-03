from typing import List, Optional

from pycubexr.classes.region import Region


class CNode(object):
    _children: List['CNode']

    def __init__(
            self,
            *,
            _id: int,
            callee_region_id: int
    ):
        self._children = []
        self.id = _id
        self.callee_region_id = callee_region_id
        self.region: Optional[Region] = None
        self.parameters = {}

    def get_children(self):
        return self._children

    def add_child(self, child: 'CNode'):
        self._children.append(child)

    def get_all_children(self, with_self=True) -> List['CNode']:
        cnodes = []
        if with_self:
            cnodes.append(self)
        for child in self._children:
            cnodes += child.get_all_children()
        return cnodes

    def __repr__(self):
        if self.region is None:
            return f'CNode<{self.id}, region_id:{self.callee_region_id}, children:{self._children}>'
        else:
            return f'CNode<{self.id}, region:<{self.callee_region_id}, {self.region.name}>, children:{self._children}>'
