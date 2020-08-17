import unittest
from pathlib import Path

from pycubexr import CubexParser
from pycubexr.utils.exceptions import MissingMetricError


class TestBlastMetricValues(unittest.TestCase):
    cubex: CubexParser = None

    @classmethod
    def setUpClass(cls) -> None:
        cubex_file_path = Path("../data/blast.p64.r1/profile.cubex").resolve()
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

    def test_time_exclusive(self):
        correct_values = [62.34447098062492, 27.709961770625, 0.05817167125, 0.052476325, 9.120066788125003,
                          0.21326868625, 10.098790139374994, 1.41302452375, 0.012670885000000002, 11.689064329375002,
                          0.15128081562499993, 0.023597896249999997, 5.620589495624999, 0.033853262499999995,
                          135.29405930187568, 0.8107423343750002, 1.01062281375, 4.435234836875001, 19.537095325624996,
                          5.26569287375, 913.5156949831248, 4.764973395625, 5.0071963725, 73.09836575000001,
                          84.50816982937499, 124.01154794124997, 160.95934515750002, 1115.03969127125,
                          5.240039464374998, 88.02404721750001, 0.031155923125, 0.011169159374999998]
        metric_values = self.get_values_for_metric('time', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_time_inclusive(self):
        correct_values = [2869.1061315206257, 27.709961770625, 0.05817167125, 0.052476325, 9.120066788125003,
                          0.21326868625, 10.098790139374994, 1.41302452375, 0.012670885000000002, 11.689064329375002,
                          0.15128081562499993, 0.023597896249999997, 5.654442758124999, 0.033853262499999995,
                          2740.5225188687505, 0.8107423343750002, 1.01062281375, 4.435234836875001, 19.537095325624996,
                          5.26569287375, 1365.8652934293748, 4.764973395625, 5.0071963725, 73.09836575000001,
                          84.50816982937499, 124.01154794124997, 160.95934515750002, 1120.279730735625,
                          5.240039464374998, 88.02404721750001, 0.031155923125, 0.011169159374999998]
        metric_values = self.get_values_for_metric('time', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_time(self):
        correct_values = [2869.1061315206257, 27.709961770625, 0.05817167125, 0.052476325, 9.120066788125003,
                          0.21326868625, 10.098790139374994, 1.41302452375, 0.012670885000000002, 11.689064329375002,
                          0.15128081562499993, 0.023597896249999997, 5.654442758124999, 0.033853262499999995,
                          2740.5225188687505, 0.8107423343750002, 1.01062281375, 4.435234836875001, 19.537095325624996,
                          5.26569287375, 1365.8652934293748, 4.764973395625, 5.0071963725, 73.09836575000001,
                          84.50816982937499, 124.01154794124997, 160.95934515750002, 1120.279730735625,
                          5.240039464374998, 88.02404721750001, 0.031155923125, 0.011169159374999998]
        metric_values = self.get_values_for_metric('time')
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_min_time_exclusive(self):
        correct_values = [44.4964743575, 0.099660839375, 1.207875E-5, 1.1459375E-5, 3.1749375E-5, 2.890375E-5,
                          2.24225E-5, 1.6657125E-4, 4.65375E-5, 2.9645E-5, 2.4228125E-5, 2.66175E-5, 0.08640601625,
                          3.1178125E-5, 0.419512393125, 1.03025E-5, 1.336625E-5, 2.3408125E-5, 4.426375E-5,
                          2.6864375E-5, 0.0995087875, 1.1555625E-5, 1.252375E-5, 2.3000625E-5, 2.7411875E-5,
                          8.3449375E-5, 4.2685E-5, 0.08285935375, 2.80325E-5, 2.8260625E-5, 7.9311875E-5, 0.0]
        metric_values = self.get_values_for_metric('min_time', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_min_time_inclusive(self):
        correct_values = [0.0, 0.099660839375, 1.207875E-5, 1.1459375E-5, 3.1749375E-5, 2.890375E-5, 2.24225E-5,
                          1.6657125E-4, 4.65375E-5, 2.9645E-5, 2.4228125E-5, 2.66175E-5, 3.1178125E-5, 3.1178125E-5,
                          1.03025E-5, 1.03025E-5, 1.336625E-5, 2.3408125E-5, 4.426375E-5, 2.6864375E-5, 1.1555625E-5,
                          1.1555625E-5, 1.252375E-5, 2.3000625E-5, 2.7411875E-5, 8.3449375E-5, 4.2685E-5, 2.80325E-5,
                          2.80325E-5, 2.8260625E-5, 7.9311875E-5, 0.0]
        metric_values = self.get_values_for_metric('min_time', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_min_time(self):
        correct_values = [44.4964743575, 0.099660839375, 1.207875E-5, 1.1459375E-5, 3.1749375E-5, 2.890375E-5,
                          2.24225E-5, 1.6657125E-4, 4.65375E-5, 2.9645E-5, 2.4228125E-5, 2.66175E-5, 0.08640601625,
                          3.1178125E-5, 0.419512393125, 1.03025E-5, 1.336625E-5, 2.3408125E-5, 4.426375E-5,
                          2.6864375E-5, 0.0995087875, 1.1555625E-5, 1.252375E-5, 2.3000625E-5, 2.7411875E-5,
                          8.3449375E-5, 4.2685E-5, 0.08285935375, 2.80325E-5, 2.8260625E-5, 7.9311875E-5, 0.0]
        metric_values = self.get_values_for_metric('min_time')
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_visits_exclusive(self):
        correct_values = [64, 64, 2752, 2560, 768, 4669, 1272, 704, 64, 768, 4410, 320, 64, 128, 6400, 51328, 51200,
                          123200, 40400, 123200, 12800, 320256, 320000, 2100000, 2100000, 320000, 627200, 12800, 25600,
                          25600, 64, 259]
        metric_values = self.get_values_for_metric('visits', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_visits_inclusive(self):
        correct_values = [6278914, 64, 2752, 2560, 768, 4669, 1272, 704, 64, 768, 4410, 320, 192, 128, 6259984, 51328,
                          51200, 123200, 40400, 123200, 5800256, 320256, 320000, 2100000, 2100000, 320000, 627200,
                          38400, 25600, 25600, 64, 259]
        metric_values = self.get_values_for_metric('visits', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_visits(self):
        correct_values = [64, 64, 2752, 2560, 768, 4669, 1272, 704, 64, 768, 4410, 320, 64, 128, 6400, 51328, 51200,
                          123200, 40400, 123200, 12800, 320256, 320000, 2100000, 2100000, 320000, 627200, 12800, 25600,
                          25600, 64, 259]
        metric_values = self.get_values_for_metric('visits')
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_max_time_exclusive(self):
        correct_values = [45.31667367375, 0.91985015625, 1.91256875E-4, 1.04669375E-4, 0.286665283125, 3.13308125E-4,
                          0.23921590875, 0.031171951875, 0.002174371875, 0.2799446225, 9.7243125E-5, 1.5729125E-4,
                          0.09052147, 0.00410541, 0.4308656325, 3.693125E-5, 4.5494375E-5, 6.1443125E-5, 0.016130028125,
                          6.4044375E-5, 0.117343304375, 4.40275E-5, 3.795375E-5, 8.400125E-5, 9.9496875E-5,
                          0.014579768125, 0.0165539275, 0.1032564775, 0.004558806875, 0.0172167, 5.7540875E-4,
                          3.887275E-4]
        metric_values = self.get_values_for_metric('max_time', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_max_time_inclusive(self):
        correct_values = [45.31667367375, 0.91985015625, 1.91256875E-4, 1.04669375E-4, 0.286665283125, 3.13308125E-4,
                          0.23921590875, 0.031171951875, 0.002174371875, 0.2799446225, 9.7243125E-5, 1.5729125E-4,
                          0.09052147, 0.00410541, 0.4308656325, 3.693125E-5, 4.5494375E-5, 6.1443125E-5, 0.016130028125,
                          6.4044375E-5, 0.117343304375, 4.40275E-5, 3.795375E-5, 8.400125E-5, 9.9496875E-5,
                          0.014579768125, 0.0165539275, 0.1032564775, 0.004558806875, 0.0172167, 5.7540875E-4,
                          3.887275E-4]
        metric_values = self.get_values_for_metric('max_time', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_max_time(self):
        correct_values = [45.31667367375, 0.91985015625, 1.91256875E-4, 1.04669375E-4, 0.286665283125, 3.13308125E-4,
                          0.23921590875, 0.031171951875, 0.002174371875, 0.2799446225, 9.7243125E-5, 1.5729125E-4,
                          0.09052147, 0.00410541, 0.4308656325, 3.693125E-5, 4.5494375E-5, 6.1443125E-5, 0.016130028125,
                          6.4044375E-5, 0.117343304375, 4.40275E-5, 3.795375E-5, 8.400125E-5, 9.9496875E-5,
                          0.014579768125, 0.0165539275, 0.1032564775, 0.004558806875, 0.0172167, 5.7540875E-4,
                          3.887275E-4]
        metric_values = self.get_values_for_metric('max_time')
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
        correct_values = [17834450945, 9377179899, 7766001, 7073976, 2501891660, 30705343, 3111693947, 352390001,
                          3824321, 3042634149, 24148644, 5432019, 1570428867, 8146408, 43653030973, 139544425,
                          136878607, 687642879, 5440289810, 773373558, 201312724939, 844010663, 829514077, 11569169175,
                          13014783021, 27194779882, 47499524979, 315991994930, 1287427729, 24577296660, 2461804,
                          1703090, ]
        metric_values = self.get_values_for_metric('PAPI_TOT_INS', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PAPI_TOT_INS_inclusive(self):
        correct_values = [732833917381, 9377179899, 7766001, 7073976, 2501891660, 30705343, 3111693947, 352390001,
                          3824321, 3042634149, 24148644, 5432019, 1578575275, 8146408, 694951986307, 139544425,
                          136878607, 687642879, 5440289810, 773373558, 302264506736, 844010663, 829514077, 11569169175,
                          13014783021, 27194779882, 47499524979, 317279422659, 1287427729, 24577296660, 2461804,
                          1703090, ]
        metric_values = self.get_values_for_metric('PAPI_TOT_INS', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PAPI_FP_INS_exclusive(self):
        correct_values = [263591229, 7808, 0, 0, 0, 0, 1815, 83369, 0, 381, 0, 107420, 178707511, 630, 2210260400, 0, 0,
                          0, 0, 0, 27830887800, 0, 0, 0, 0, 0, 617400, 36675220160, 126000, 25603, 0, 0, ]
        metric_values = self.get_values_for_metric('PAPI_FP_INS', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PAPI_FP_INS_inclusive(self):
        correct_values = [67159637526, 7808, 0, 0, 0, 0, 1815, 83369, 0, 381, 0, 107420, 178708141, 630, 66717137363, 0,
                          0, 0, 0, 0, 27831505200, 0, 0, 0, 0, 0, 617400, 36675346160, 126000, 25603, 0, 0, ]
        metric_values = self.get_values_for_metric('PAPI_FP_INS', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PAPI_FP_OPS_exclusive(self):
        correct_values = [350299766, 7680, 0, 0, 0, 0, 1800, 82680, 0, 378, 0, 161798, 281315484, 378, 2933699878, 0, 0,
                          0, 0, 0, 55720155160, 0, 0, 0, 0, 0, 617400, 57548356630, 75746, 25200, 0, 0, ]
        metric_values = self.get_values_for_metric('PAPI_FP_OPS', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PAPI_FP_OPS_inclusive(self):
        correct_values = [116834799978, 7680, 0, 0, 0, 0, 1800, 82680, 0, 378, 0, 161798, 281315862, 378, 116202930014,
                          0, 0, 0, 0, 0, 55720772560, 0, 0, 0, 0, 0, 617400, 57548432376, 75746, 25200, 0, 0, ]
        metric_values = self.get_values_for_metric('PAPI_FP_OPS', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PEVT_L2_FETCH_LINE_exclusive(self):
        correct_values = [328414128, 25908052, 1681098, 1265551, 1528254, 4634061, 31674740, 14600717, 57948, 18592760,
                          1896267, 696772, 29910682, 301408, 7335784630, 32563515, 51893248, 181917020, 1002903446,
                          356364049, 129974076443, 120889884, 260817847, 1911357194, 4624351825, 13703857246,
                          5524580067, 6512175761, 72589748, 349479677, 679460, 148940, ]
        metric_values = self.get_values_for_metric('PEVT_L2_FETCH_LINE', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PEVT_L2_FETCH_LINE_inclusive(self):
        correct_values = [172477592438, 25908052, 1681098, 1265551, 1528254, 4634061, 31674740, 14600717, 57948,
                          18592760, 1896267, 696772, 30212090, 301408, 172015601600, 32563515, 51893248, 181917020,
                          1002903446, 356364049, 156119930506, 120889884, 260817847, 1911357194, 4624351825,
                          13703857246, 5524580067, 6584765509, 72589748, 349479677, 679460, 148940, ]
        metric_values = self.get_values_for_metric('PEVT_L2_FETCH_LINE', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PEVT_L2_STORE_LINE_exclusive(self):
        correct_values = [290435817, 128816424, 1119542, 1135450, 862320, 4371690, 21399957, 10361966, 32807, 10121287,
                          1267895, 438347, 7370608, 83635, 2279264531, 10994192, 15606608, 60855524, 269961065,
                          122639308, 21541673924, 21329822, 36161911, 287597475, 430541107, 2466248882, 980045302,
                          1719174203, 22322286, 71382678, 322859, 534062, ]
        metric_values = self.get_values_for_metric('PEVT_L2_STORE_LINE', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_PEVT_L2_STORE_LINE_inclusive(self):
        correct_values = [30814473484, 128816424, 1119542, 1135450, 862320, 4371690, 21399957, 10361966, 32807,
                          10121287, 1267895, 438347, 7454243, 83635, 30335798818, 10994192, 15606608, 60855524,
                          269961065, 122639308, 25763598423, 21329822, 36161911, 287597475, 430541107, 2466248882,
                          980045302, 1741496489, 22322286, 71382678, 322859, 534062, ]
        metric_values = self.get_values_for_metric('PEVT_L2_STORE_LINE', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_bytes_sent_exclusive(self):
        correct_values = [0, 0, 0, 0, 2496, 1391628, 0, 180224, 512, 294912, 0, 326144, 0, 2816, 0, 0, 0, 0, 0,
                          52595200, 0, 0, 0, 0, 875840000, 0, 321126400, 0, 563200, 13107200, 0, 0, ]
        metric_values = self.get_values_for_metric('bytes_sent', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_bytes_sent_inclusive(self):
        correct_values = [1265430732, 0, 0, 0, 2496, 1391628, 0, 180224, 512, 294912, 0, 326144, 2816, 2816, 1263232000,
                          0, 0, 0, 0, 52595200, 1196966400, 0, 0, 0, 875840000, 0, 321126400, 563200, 563200, 13107200,
                          0, 0, ]
        metric_values = self.get_values_for_metric('bytes_sent', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_bytes_received_exclusive(self):
        correct_values = [0, 0, 0, 0, 2496, 0, 1387344, 180224, 512, 294912, 0, 326144, 0, 2816, 0, 0, 0, 0, 52595200,
                          0, 0, 0, 0, 0, 0, 875840000, 321126400, 0, 563200, 13107200, 0, 4284, ]
        metric_values = self.get_values_for_metric('bytes_received', convert_to_exclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)

    def test_bytes_received_inclusive(self):
        correct_values = [1265430732, 0, 0, 0, 2496, 0, 1387344, 180224, 512, 294912, 0, 326144, 2816, 2816, 1263232000,
                          0, 0, 0, 52595200, 0, 1196966400, 0, 0, 0, 0, 875840000, 321126400, 563200, 563200, 13107200,
                          0, 4284, ]
        metric_values = self.get_values_for_metric('bytes_received', convert_to_inclusive=True)
        for correct, cnode_values in zip(correct_values, metric_values):
            self.assertAlmostEqual(correct, cnode_values)


if __name__ == '__main__':
    unittest.main()
