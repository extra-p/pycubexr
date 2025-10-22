# This file is part of the Extra-P software (http://www.scalasca.org/software/extra-p)
#
# Copyright (c) 2020-2022, Technical University of Darmstadt, Germany
#
# This software may be modified and distributed under the terms of a BSD-style license.
# See the LICENSE file in the base directory for details.

import unittest
from pathlib import Path
from unittest import SkipTest

from pycubexr import CubexParser


class TestExtendedCudaKernels(unittest.TestCase):
    cubex: CubexParser = None

    @classmethod
    def setUpClass(cls) -> None:
        try:
            cubex_file_path = Path("../data/cube_samples/profile_extended_kernel.cubex").resolve(strict=True)
        except FileNotFoundError as err:
            raise SkipTest("Required test file was not found.") from err
        cls.cubex = CubexParser(cubex_file_path).__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.cubex.__exit__(None, None, None)

    def test_method_names_not_mangled(self):
        cnodes = self.cubex.all_cnodes()
        print(cnodes[15].region.name)


if __name__ == '__main__':
    unittest.main()
