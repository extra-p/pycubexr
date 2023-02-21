import unittest
from pathlib import Path
from unittest import SkipTest

from pycubexr import CubexParser


class TestCube4_8WithBug(unittest.TestCase):

    def test_load(self):
        try:
            cubex_file_path = Path("../data/cube_samples/cube4.8_with_checksum_bug.cubex").resolve()
            with self.assertWarnsRegex(UserWarning, "checksum"):
                with CubexParser(cubex_file_path) as cube_file:
                    cube_file.all_metrics()
        except FileNotFoundError as err:
            raise SkipTest("Required test file was not found.") from err


if __name__ == '__main__':
    unittest.main()
