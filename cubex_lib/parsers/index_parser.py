import struct
from typing import List, BinaryIO


class IndexParser(object):
    cnode_indices: List[int]
    HEADER: bytes = b'CUBEX.INDEX'

    def __init__(self, index_file: BinaryIO):
        self.cnode_indices = []
        self.endianness_fmt = '<'
        self._index_file = index_file
        self._read_index()

    def _read_index(self):
        assert not self._index_file.closed

        header = self._index_file.read(len(self.HEADER))
        assert header == self.HEADER

        # The index file starts with the number 1 encoded as an int.
        # Here, we parse it to determine the endianness of the machine that created the index file.
        one = struct.unpack('<i', self._index_file.read(4))[0]

        # If the "one" is parsed as a 1, the endianness "<" format is right - else flip it.
        # Important: the endianness must also be used for the data file!
        self.endianness_fmt = '<' if one == 1 else '>'

        # IMPORTANT: not used but MUST not be deleted!
        # noinspection PyUnusedLocal
        version = struct.unpack('{}h'.format(self.endianness_fmt), self._index_file.read(2))[0]
        # noinspection PyUnusedLocal
        index_type = self._index_file.read(1)

        # Parse how many indices this file contains
        raw_size = self._index_file.read(4)
        n_nodes = struct.unpack('{}i'.format(self.endianness_fmt), raw_size)[0]

        raw_index = self._index_file.read()

        index_value_size = struct.calcsize("i")
        if len(raw_index) != index_value_size * n_nodes:
            raise Exception("The size of the index list should equal to (size of one index value * number of nodes).")
        self.cnode_indices = list(struct.unpack('{}{}i'.format(self.endianness_fmt, n_nodes), raw_index))
        assert len(self.cnode_indices) > 0
        assert self._index_file.peek() == b''
