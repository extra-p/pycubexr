# This file is part of the Extra-P software (http://www.scalasca.org/software/extra-p)
#
# Copyright (c) 2020-2022, Technical University of Darmstadt, Germany
#
# This software may be modified and distributed under the terms of a BSD-style license.
# See the LICENSE file in the base directory for details.

import unittest
from pathlib import Path

from pycubexr import CubexParser


class TestLuleshMethodNames(unittest.TestCase):
    cubex: CubexParser = None

    @classmethod
    def setUpClass(cls) -> None:
        cubex_file_path = Path("../data/lulesh.s64/profile.cubex").resolve()
        cls.cubex = CubexParser(cubex_file_path).__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.cubex.__exit__(None, None, None)

    def test_method_names_not_mangled(self):
        cnodes = self.cubex.all_cnodes()
        print(cnodes[15].region.name)


if __name__ == '__main__':
    unittest.main()
