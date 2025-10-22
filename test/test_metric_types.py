import unittest
from pathlib import Path
from typing import Callable

import numpy as np

from pycubexr import CubexParser
from pycubexr.utils.exceptions import UnsupportedMetricFormatError
from pycubexr.utils.metric_formats import METRIC_FORMATS


class TestMetricTypes(unittest.TestCase):
    def test_list_of_metric_types(self):
        for metric_type in METRIC_FORMATS.values():
            if isinstance(metric_type, Callable):
                metric_type = metric_type('5')

            print(metric_type)
            test = np.dtype(metric_type)
            print(metric_type, ':', test)

    def test_metric_types(self):
        cubex_file_path = Path("../data/test_only_files/cube-values_example.cubex").resolve()
        with CubexParser(cubex_file_path) as cubex:
            for metric in cubex.get_metrics():
                with self.subTest(metric=metric.name):
                    if metric.name == "HISTOGRAM5":
                        self.assertEqual("HISTOGRAM(5)", metric.data_type)
                    elif metric.name == "NDOUBLES10":
                        self.assertEqual("NDOUBLES(10)", metric.data_type)
                    elif metric.name == "SCALE_FUNC3":
                        self.assertEqual("SCALE_FUNC", metric.data_type)
                    elif metric.name == "TAU_ATOMIC2":
                        self.assertEqual("TAU_ATOMIC", metric.data_type)
                    else:
                        self.assertEqual(metric.name, metric.data_type)

    def test_parsing(self):
        cubex_file_path = Path("../data/test_only_files/cube-values_example.cubex").resolve()
        with CubexParser(cubex_file_path) as cubex:
            for metric in cubex.get_metrics():
                with self.subTest(metric=metric.name):
                    if metric.name in ["HISTOGRAM5", "SCALE_FUNC3"]:
                        self.assertRaises(UnsupportedMetricFormatError, cubex.get_metric_values, metric)
                    else:
                        cubex.get_metric_values(metric)


if __name__ == '__main__':
    unittest.main()
