from pathlib import Path

import unittest

from pycubexr import CubexParser


class TestCube4_8WithBug(unittest.TestCase):

    def test_load(self):
        cubex_file_path = Path("../data/bt-mz_sum.p2.r1/cube4.8_with_checksum_bug.cubex").resolve()
        with self.assertWarnsRegex(UserWarning, "checksum"):
            with CubexParser(cubex_file_path) as cube_file:
                cube_file.all_metrics()


if __name__ == '__main__':
    unittest.main()
