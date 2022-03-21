class Region(object):

    def __init__(
            self,
            *,
            _id: int,
            begin: int,
            end: int,
            name: str,
            mangled_name: str,
            paradigm: str,
            role: str,
            url: str,
            descr: str,
            mod: str
    ):
        self.id = _id
        self.begin = begin
        self.end = end
        self.name = name
        self.mangled_name = mangled_name
        self.paradigm = paradigm
        self.role = role
        self.url = url
        self.description = descr
        self.mod = mod

    def __repr__(self):
        return 'Region<{}>'.format(self.__dict__)
