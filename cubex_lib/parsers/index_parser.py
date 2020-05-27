import struct
from typing import List, BinaryIO, Any


class CubexIndexParser(object):
    endianness_fmt: str
    cnode_indices: List[Any]
    HEADER: bytes = b'CUBEX.INDEX'

    # TODO: this SHOULD be static
    def __init__(self, index_file: BinaryIO):
        assert not index_file.closed

        header = index_file.read(len(self.HEADER))
        assert header == self.HEADER

        # The index file starts with the number 1 encoded as an int.
        # Here, we parse it to determine the endianness of the machine that created the index file.
        one = struct.unpack('<i', index_file.read(4))[0]

        # If the "one" is parsed as a 1, the endianness "<" format is right - else flip it.
        # Important: the endianness must also be used for the data file!
        self.endianness_fmt = '<' if one == 1 else '>'

        # IMPORTANT: not used but MUST not be deleted!
        # noinspection PyUnusedLocal
        version = struct.unpack('{}h'.format(self.endianness_fmt), index_file.read(2))[0]
        # noinspection PyUnusedLocal
        index_type = index_file.read(1)

        # Parse how many indices this file contains
        raw_size = index_file.read(4)
        n_nodes = struct.unpack('{}i'.format(self.endianness_fmt), raw_size)[0]

        raw_index = index_file.read()

        index_value_size = struct.calcsize("i")
        if len(raw_index) != index_value_size * n_nodes:
            raise Exception("The size of the index list should equal to (size of one index value * number of nodes).")

        self.cnode_indices = list(struct.unpack('{}{}i'.format(self.endianness_fmt, n_nodes), raw_index))
        assert len(self.cnode_indices) > 0
        assert index_file.peek() == b''
