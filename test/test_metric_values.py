import csv
import io
import unittest
from itertools import groupby
from operator import itemgetter
from pathlib import Path
from zipfile import ZipFile

from pycubexr import CubexParser
from pycubexr.classes.values import CubeValues
from pycubexr.utils.exceptions import MissingMetricError


class TestMetricValues(unittest.TestCase):
    def test_time_example(self):
        cubex_file_path = Path("../data/time.p4.n2000.x1.r0/profile.cubex").resolve()
        excl_file_path = Path("../data/time.p4.n2000.x1.r0/excl.csv").resolve()
        incl_file_path = Path("../data/time.p4.n2000.x1.r0/incl.csv").resolve()
        with CubexParser(cubex_file_path) as cubex:
            with open(excl_file_path) as excl:
                self.check_against_csv_dump(cubex, excl)
            with open(incl_file_path) as incl:
                self.check_against_csv_dump(cubex, incl, inclusive=True)

    def test_call_tree_example(self):
        cubex_file_path = Path("../data/call_tree_test/call_tree_test.cubex").resolve()
        excl_file_path = Path("../data/call_tree_test/excl.csv").resolve()
        incl_file_path = Path("../data/call_tree_test/incl.csv").resolve()
        with CubexParser(cubex_file_path) as cubex:
            with open(excl_file_path) as excl:
                self.check_against_csv_dump(cubex, excl)
            with open(incl_file_path) as incl:
                self.check_against_csv_dump(cubex, incl, inclusive=True)

    def test_blast_example(self):
        cubex_file_path = Path("../data/blast.p64.r1/profile.cubex").resolve()
        excl_file_path = Path("../data/blast.p64.r1/excl.csv").resolve()
        incl_file_path = Path("../data/blast.p64.r1/incl.csv").resolve()
        with CubexParser(cubex_file_path) as cubex:
            with open(excl_file_path) as excl:
                self.check_against_csv_dump(cubex, excl)
            with open(incl_file_path) as incl:
                self.check_against_csv_dump(cubex, incl, inclusive=True)

    def test_miniFE_example(self):
        cubex_file_path = Path("../data/miniFE/profile.cubex").resolve()
        csv_file_path = Path("../data/miniFE/csv.zip").resolve()
        with CubexParser(cubex_file_path) as cubex, ZipFile(csv_file_path) as csv_zip:
            with csv_zip.open("excl.csv") as excl:
                self.check_against_csv_dump(cubex, io.TextIOWrapper(excl, encoding='utf-8', newline=''))
            with csv_zip.open("incl.csv") as incl:
                self.check_against_csv_dump(cubex, io.TextIOWrapper(incl, encoding='utf-8', newline=''), inclusive=True)

    def check_against_csv_dump(self, cubex, csv_dump, inclusive=False):
        csvreader = csv.reader(csv_dump)
        metrics = next(csvreader)  # read header
        for metric_index, metric_name in enumerate(metrics):
            if metric_index < 2:
                continue  # skip first two columns
            with self.subTest(metric=metric_name, inclusive=inclusive):
                metric = cubex.get_metric_by_name(metric_name)
                self.assertNotEqual(metric, None)
                csv_dump.seek(0)
                next(csvreader)  # skip header
                try:
                    metric_values = cubex.get_metric_values(metric, allow_full_uint64_values=True)
                    for cnode_id, rows in groupby(csvreader, itemgetter(0)):
                        cnode = cubex.get_cnode(int(cnode_id))
                        self.assertNotEqual(cnode, None)

                        values = metric_values.cnode_values(cnode, convert_to_exclusive=not inclusive,
                                                            convert_to_inclusive=inclusive)

                        original_values = [row[metric_index] for row in rows]
                        self.assertEqual(len(values), len(original_values),
                                         msg=f"at {metric_name} for cnode {cnode_id}")
                        for original_value, value in zip(original_values, values):
                            try:
                                if isinstance(value, CubeValues):
                                    value = value.astype(float)
                                pos_dot = original_value.rfind('.')
                                pos_e = original_value.find('e')
                                if pos_e >= 0:
                                    places = pos_e - pos_dot - 1
                                else:
                                    places = len(original_value) - 1 - pos_dot - 1
                                self.assertAlmostEqual(float(original_value), value, places=places,
                                                       msg=f"at {metric_name} for cnode {cnode_id} {cnode.region.name}: expected {original_value} got {value}")
                            except AssertionError:
                                raise
                except MissingMetricError:
                    self.assertTrue(all(int(r[metric_index]) == 0 for r in csvreader),
                                    msg=f"Metric {metric_name} was signaled as missing even though it should contain "
                                        f"values.")
