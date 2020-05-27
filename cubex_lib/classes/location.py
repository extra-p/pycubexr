class Location(object):
    def __init__(
            self,
            *,
            _id: int,
            name: str,
            rank: str,
            _type: str
    ):
        self.id = _id
        self.name = name
        self.rank = rank
        self.type = _type

    def __repr__(self):
        return 'Location<{}>'.format(self.__dict__)
