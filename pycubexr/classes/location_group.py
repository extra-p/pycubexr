from typing import List

from pycubexr.classes import Location


class LocationGroup(object):
    _location_groups: List['LocationGroup']
    _locations: List[Location]

    def __init__(self, *, _id: int, name: str, rank: int, _type: str):
        self._location_groups = []
        self._locations = []
        self.id = _id
        self.name = name
        self.rank = rank
        self.type = _type

    def all_locations(self):
        locations = [x for x in self._locations]
        for location_group in self._location_groups:
            locations += location_group.all_locations()
        return locations

    def add_location_group(self, child: 'LocationGroup'):
        self._location_groups.append(child)

    def add_location(self, child: Location):
        self._locations.append(child)

    def __repr__(self):
        return 'LocationGroup<{}>'.format(self.__dict__)
