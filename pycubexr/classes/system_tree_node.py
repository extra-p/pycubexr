import typing
from typing import List

from pycubexr.classes import LocationGroup, Location


class SystemTreeNode(object):
    _system_tree_node_children: List['SystemTreeNode']
    _location_group_children: List[LocationGroup]

    def __init__(
            self,
            *,
            _id: int,
            _class: str,
            name: str,
            attrs: typing.Dict[str, str]
    ):
        self._system_tree_node_children = []
        self._location_group_children = []
        self.id = _id
        self.clazz = _class
        self.name = name
        self.attrs = attrs

    def all_location_groups(self) -> List[LocationGroup]:
        location_groups = [x for x in self._location_group_children]
        for system_tree_child in self._system_tree_node_children:
            location_groups += system_tree_child.all_location_groups()
        return location_groups

    def all_locations(self) -> List[Location]:
        locations: List[Location] = []
        for location_group in self.all_location_groups():
            locations += location_group.all_locations()
        return locations

    def add_system_tree_node_child(self, child: 'SystemTreeNode'):
        self._system_tree_node_children.append(child)

    def add_location_group(self, child: LocationGroup):
        self._location_group_children.append(child)

    def __repr__(self):
        return 'SystemTreeNode<{}>'.format(self.__dict__)
