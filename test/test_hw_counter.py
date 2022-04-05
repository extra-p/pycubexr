import unittest
from pathlib import Path

from pycubexr import CubexParser


class TestHWCounterMeasurements1(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cubex_file_path = Path("../data/hw_counter/L2_DCM_negative.cubex").resolve()
        cls.cubex = CubexParser(cubex_file_path).__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.cubex.__exit__(None, None, None)

    def get_values_for_metric(self, name, convert_to_exclusive=False, convert_to_inclusive=False):
        metric = self.cubex.get_metric_by_name(name)
        metric_values = self.cubex.get_metric_values(metric)
        # iterate over all callpaths in cubex file
        cnode_values = []
        for cnode in self.cubex.all_cnodes():
            # return the measurement values for all mpi processes for the current metric and callpath
            value = metric_values.value(cnode, convert_to_exclusive, convert_to_inclusive)
            cnode_values.append(value)
        return cnode_values

    def test_PAPI_L2_DCM_exclusive(self):
        metric_values = self.get_values_for_metric('PAPI_L2_DCM', convert_to_exclusive=True)
        for cnode_value in metric_values:
            self.assertGreaterEqual(cnode_value, 0)
            self.assertLess(cnode_value, 0xFFFFFFFFFFFFFFFF)

    def test_PAPI_L2_DCM_inclusive(self):
        metric_values = self.get_values_for_metric('PAPI_L2_DCM', convert_to_inclusive=True)
        for cnode_value in metric_values:
            self.assertGreaterEqual(cnode_value, 0)
            self.assertLess(cnode_value, 0xFFFFFFFFFFFFFFFF)

    def test_PAPI_L2_DCM_allow_full_uint64(self):
        metric = self.cubex.get_metric_by_name('PAPI_L2_DCM')
        metric_values = self.cubex.get_metric_values(metric, allow_full_uint64_values=True)
        values = [metric_values.value(cnode) for cnode in self.cubex.all_cnodes()]
        self.assertTrue(all(v >= 0 for v in values))
        self.assertTrue(any(v >= 0xFFFF_FFFF_FFFF_FFFF for v in values))


class TestHWCounterMeasurements2(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cubex_file_path = Path("../data/hw_counter/L3_DCA_negative.cubex").resolve()
        cls.cubex = CubexParser(cubex_file_path).__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.cubex.__exit__(None, None, None)

    def get_values_for_metric(self, name, convert_to_exclusive=False, convert_to_inclusive=False):
        metric = self.cubex.get_metric_by_name(name)
        metric_values = self.cubex.get_metric_values(metric)
        # iterate over all callpaths in cubex file
        cnode_values = []
        for cnode in self.cubex.all_cnodes():
            # return the measurement values for all mpi processes for the current metric and callpath
            value = metric_values.value(cnode, convert_to_exclusive, convert_to_inclusive)
            self.assertGreaterEqual(value, 0)
            cnode_values.append(value)
        return cnode_values

    def test_PAPI_L2_DCM_exclusive(self):
        metric_values = self.get_values_for_metric('PAPI_L3_DCA', convert_to_exclusive=True)
        for cnode_value in metric_values:
            self.assertGreaterEqual(cnode_value, 0)
            self.assertLess(cnode_value, 0xFFFFFFFFFFFFFFFF)

    def test_PAPI_L2_DCM_inclusive(self):
        metric_values = self.get_values_for_metric('PAPI_L3_DCA', convert_to_inclusive=True)
        for cnode_value in metric_values:
            self.assertGreaterEqual(cnode_value, 0)
            self.assertLess(cnode_value, 0xFFFFFFFFFFFFFFFF)


if __name__ == '__main__':
    unittest.main()
