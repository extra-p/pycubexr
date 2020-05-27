import typing


class CNode(object):
    _children: typing.List['CNode']

    def __init__(
            self,
            *,
            _id: int,
            callee_region_id: int
    ):
        self._children = []
        self.id = _id
        self.callee_region_id = callee_region_id

    def add_child(self, child: 'CNode'):
        self._children.append(child)

    def get_all_children(self) -> typing.List['CNode']:
        cnodes = [self]
        for child in self._children:
            cnodes += child.get_all_children()
        return cnodes

    def __repr__(self):
        return 'CNode<{}>'.format(self.__dict__)