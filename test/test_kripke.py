import unittest
from pathlib import Path

from pycubexr import CubexParser
from pycubexr.utils.exceptions import MissingMetricError


class TestMetricValuesKripke(unittest.TestCase):
    cubex: CubexParser = None

    @classmethod
    def setUpClass(cls) -> None:
        cubex_file_path = Path("../data/kripke.p8.d2.g32.r1/profile.cubex").resolve()
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
            cnode_values.append(metric_values.value(cnode, convert_to_exclusive, convert_to_inclusive))
        return cnode_values

    def test_visits_exclusive(self):
        correct_values = [8, 8, 33, 16, 8, 8000, 8000, 8000, 8000, 96000, 169025, 96000, 8000, 8, ]
        metric_values = self.get_values_for_metric('visits', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_visits_inclusive(self):
        correct_values = [401106, 8, 33, 16, 401033, 8000, 8000, 385025, 8000, 96000, 169025, 96000, 8000, 8, ]
        metric_values = self.get_values_for_metric('visits', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_time_exclusive(self):
        correct_values = [0.049351889999996956, 0.41779200749999995, 4.7357375E-4, 1.7047999999999998E-4,
                          0.4765991312500262, 59.994445453124996, 59.901360724375, 18.81082184375, 0.0791653,
                          1.9761004281249999, 3.677575010625, 2.70347292125, 0.5036856562500001, 0.04049549125, ]
        metric_values = self.get_values_for_metric('time', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_time_inclusive(self):
        correct_values = [148.63150991125, 0.41779200749999995, 4.7357375E-4, 1.7047999999999998E-4, 148.12322646875,
                          59.994445453124996, 59.901360724375, 27.750821159999997, 0.0791653, 1.9761004281249999,
                          3.677575010625, 2.70347292125, 0.5036856562500001, 0.04049549125, ]
        metric_values = self.get_values_for_metric('time', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_min_time_exclusive(self):
        correct_values = [18.57139089625, 0.0446771925, 5.263125E-6, 5.80125E-6, 18.5020277025, 0.00741907125,
                          0.00703084, 0.00325334125, 7.605E-6, 1.7570625E-5, 7.595E-6, 2.031375E-5, 5.414375E-5,
                          4.776875E-5, ]
        metric_values = self.get_values_for_metric('min_time', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_min_time_inclusive(self):
        correct_values = [5.263125E-6, 0.0446771925, 5.263125E-6, 5.80125E-6, 7.595E-6, 0.00741907125, 0.00703084,
                          7.595E-6, 7.605E-6, 1.7570625E-5, 7.595E-6, 2.031375E-5, 5.414375E-5, 4.776875E-5, ]
        metric_values = self.get_values_for_metric('min_time', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_max_time_exclusive(self):
        correct_values = [18.60063626375, 0.073913345, 6.36525E-5, 3.40825E-5, 18.51830332, 0.008342615, 0.00768267875,
                          0.0177915775, 1.236375E-5, 6.542625E-5, 1.2951E-4, 7.841E-5, 8.488E-5, 0.00588251125, ]
        metric_values = self.get_values_for_metric('max_time', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_max_time_inclusive(self):
        correct_values = [18.60063626375, 0.073913345, 6.36525E-5, 3.40825E-5, 18.51830332, 0.008342615, 0.00768267875,
                          0.0177915775, 1.236375E-5, 6.542625E-5, 1.2951E-4, 7.841E-5, 8.488E-5, 0.00588251125, ]
        metric_values = self.get_values_for_metric('max_time', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_task_migration_loss(self):
        self.assertRaises(MissingMetricError, self.get_values_for_metric, 'task_migration_loss',
                          convert_to_exclusive=True)
        self.assertRaises(MissingMetricError, self.get_values_for_metric, 'task_migration_loss',
                          convert_to_inclusive=True)

    def test_task_migration_win(self):
        self.assertRaises(MissingMetricError, self.get_values_for_metric, 'task_migration_win',
                          convert_to_exclusive=True)
        self.assertRaises(MissingMetricError, self.get_values_for_metric, 'task_migration_win',
                          convert_to_inclusive=True)

    def test_bytes_put(self):
        self.assertRaises(MissingMetricError, self.get_values_for_metric, 'bytes_put', convert_to_exclusive=True)
        self.assertRaises(MissingMetricError, self.get_values_for_metric, 'bytes_put', convert_to_inclusive=True)

    def test_bytes_get(self):
        self.assertRaises(MissingMetricError, self.get_values_for_metric, 'bytes_get', convert_to_exclusive=True)
        self.assertRaises(MissingMetricError, self.get_values_for_metric, 'bytes_get', convert_to_inclusive=True)

    def test_PAPI_TOT_INS_exclusive(self):
        correct_values = [16380495, 218090062, 82702, 41913, 92374590, 18428764176, 18440603145, 4575020158, 20131404,
                          550715334, 919093540, 580021611, 131607814, 9039208, ]
        metric_values = self.get_values_for_metric('PAPI_TOT_INS', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PAPI_TOT_INS_inclusive(self):
        correct_values = [43981966152, 218090062, 82702, 41913, 43738331772, 18428764176, 18440603145, 6776589861,
                          20131404, 550715334, 919093540, 580021611, 131607814, 9039208, ]
        metric_values = self.get_values_for_metric('PAPI_TOT_INS', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PAPI_FP_INS_exclusive(self):
        correct_values = [2135, 496, 0, 0, 144000, 2764800000, 2764800000, 1109152000, 0, 0, 0, 0, 0, 0, ]
        metric_values = self.get_values_for_metric('PAPI_FP_INS', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PAPI_FP_INS_inclusive(self):
        correct_values = [6638898631, 496, 0, 0, 6638896000, 2764800000, 2764800000, 1109152000, 0, 0, 0, 0, 0, 0, ]
        metric_values = self.get_values_for_metric('PAPI_FP_INS', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PAPI_FP_OPS_exclusive(self):
        correct_values = [2183, 480, 0, 0, 144000, 5529600000, 5529600000, 2697987161, 0, 0, 0, 0, 0, 0, ]
        metric_values = self.get_values_for_metric('PAPI_FP_OPS', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PAPI_FP_OPS_inclusive(self):
        correct_values = [13757333824, 480, 0, 0, 13757331161, 5529600000, 5529600000, 2697987161, 0, 0, 0, 0, 0, 0, ]
        metric_values = self.get_values_for_metric('PAPI_FP_OPS', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PEVT_L2_FETCH_LINE_exclusive(self):
        correct_values = [236294, 301627, 2475, 466, 9951320, 63665366, 621100937, 72281973, 484451, 14599752, 16286754,
                          7812501, 1204831, 8663, ]
        metric_values = self.get_values_for_metric('PEVT_L2_FETCH_LINE', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PEVT_L2_FETCH_LINE_inclusive(self):
        correct_values = [807937410, 301627, 2475, 466, 807387885, 63665366, 621100937, 112670262, 484451, 14599752,
                          16286754, 7812501, 1204831, 8663, ]
        metric_values = self.get_values_for_metric('PEVT_L2_FETCH_LINE', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PEVT_L2_STORE_LINE_exclusive(self):
        correct_values = [2279935, 2075179, 6347, 509, 12419687, 131884217, 761931928, 456598356, 980669, 47246817,
                          101259237, 55485219, 22286633, 6776, ]
        metric_values = self.get_values_for_metric('PEVT_L2_STORE_LINE', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PEVT_L2_STORE_LINE_inclusive(self):
        correct_values = [1594461509, 2075179, 6347, 509, 1590092763, 131884217, 761931928, 683856931, 980669, 47246817,
                          101259237, 55485219, 22286633, 6776, ]
        metric_values = self.get_values_for_metric('PEVT_L2_STORE_LINE', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_bytes_sent_exclusive(self):
        correct_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1770240000, 0, 0, ]
        metric_values = self.get_values_for_metric('bytes_sent', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_bytes_sent_inclusive(self):
        correct_values = [1770240000, 0, 0, 0, 1770240000, 0, 0, 1770240000, 0, 0, 0, 1770240000, 0, 0, ]
        metric_values = self.get_values_for_metric('bytes_sent', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_bytes_received_exclusive(self):
        correct_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1770240000, 0, 0, 0, ]
        metric_values = self.get_values_for_metric('bytes_received', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_bytes_received_inclusive(self):
        correct_values = [1770240000, 0, 0, 0, 1770240000, 0, 0, 1770240000, 0, 0, 1770240000, 0, 0, 0, ]
        metric_values = self.get_values_for_metric('bytes_received', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)


if __name__ == '__main__':
    unittest.main()
