import unittest
from pathlib import Path

from pycubexr import CubexParser
from pycubexr.classes.metric import MetricType
from pycubexr.utils.exceptions import MissingMetricError


class TestBasicCallTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cubex_file_path = Path("../data/call_tree_test/call_tree_test.cubex").resolve()
        cls.cubex = CubexParser(cubex_file_path).__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.cubex.__exit__(None, None, None)

    def test_root_cnode(self):
        root_cnode = self.cubex.get_root_cnodes()
        self.assertEqual(len(root_cnode), 1)
        self.assertEqual(0, root_cnode[0].id)
        self.assertEqual('test.x', root_cnode[0].region.name)
        self.assertEqual(2, root_cnode[0].region.id)

    def test_callpaths(self):
        callpaths = self._walk_cnode_tree(self.cubex.get_root_cnodes())
        expected_callpaths = {i: v for i, v in enumerate([
            "test.x",
            "test.x->main",
            "test.x->main->a",
            "test.x->main->a->a1",
            "test.x->main->a->a2",
            "test.x->main->a->a3",
            "test.x->main->b",
            "test.x->main->b->b1",
            "test.x->main->b->b2",
            "test.x->main->b->b3",
            "test.x->main->c",
            "test.x->main->c->c1",
            "test.x->main->c->c2",
            "test.x->main->c->c3",
            "test.x->main->d",
            "test.x->main->d->d1",
            "test.x->main->d->d2",
            "test.x->main->d->d3",
        ])}
        self.assertDictEqual(expected_callpaths, callpaths)

    def test_cnodes(self):
        expected_cnodes = [
            "cube_test_file/test.x",
            "main",
            "a",
            "a1",
            "a2",
            "a3",
            "b",
            "b1",
            "b2",
            "b3",
            "c",
            "c1",
            "c2",
            "c3",
            "d",
            "d1",
            "d2",
            "d3",
        ]
        for i, v in enumerate(expected_cnodes):
            cnode = self.cubex.get_cnode(i)
            self.assertEqual(v, cnode.region.mangled_name)

    def _walk_cnode_tree(self, cnodes):

        callpaths = {}

        def walk_tree(parent_cnode, parent_name, level):
            num_nodes_per_level = {0: 1, 1: 4, 2: 3, 3: 0}
            self.assertEqual(len(parent_cnode.get_children()), num_nodes_per_level[level])

            for cnode in parent_cnode.get_children():
                name = cnode.region.mangled_name
                path_name = '->'.join((parent_name, name))
                callpath = path_name
                callpaths[cnode.id] = callpath
                walk_tree(cnode, path_name, level + 1)

        for root_cnode in cnodes:
            name = root_cnode.region.name
            callpath = name
            callpaths[root_cnode.id] = callpath
            walk_tree(root_cnode, name, 0)

        return callpaths

    def test_metrics(self):
        metrics = ['visits', 'time', 'min_time', 'max_time', 'bytes_put', 'bytes_get', 'io_bytes_read',
                   'io_bytes_written']
        metric_types = [MetricType.EXCLUSIVE, MetricType.INCLUSIVE, MetricType.EXCLUSIVE, MetricType.EXCLUSIVE,
                        MetricType.EXCLUSIVE, MetricType.EXCLUSIVE, MetricType.EXCLUSIVE, MetricType.EXCLUSIVE]
        for i, cube_metric in enumerate(self.cubex.get_metrics()):
            self.assertEqual(cube_metric.name, metrics[i])
            self.assertEqual(i, cube_metric.id)
            self.assertEqual(cube_metric.metric_type, metric_types[i])

    def test_values_visits(self):
        metric = self.cubex.get_metric_by_name('visits')
        metric_values = self.cubex.get_metric_values(metric, cache=False)
        expected_values = [
            1,
            1,
            1,
            1, 2, 3,
            2,
            2, 4, 6,
            3,
            3, 6, 9,
            4,
            4, 8, 12,
        ]
        for i, v in enumerate(expected_values):
            cnode = self.cubex.get_cnode(i)
            values = metric_values.cnode_values(cnode)
            self.assertEqual(v, values[0])

    def test_values_time(self):
        metric = self.cubex.get_metric_by_name('time')
        metric_values = self.cubex.get_metric_values(metric, cache=False)
        expected_values = [
            74.05,
            74.05,
            60.00,
            10.0, 20.0, 30.0,
            12.00,
            2.0, 4.0, 6.0,
            1.80,
            0.3, 0.6, 0.9,
            0.24,
            0.04, 0.08, 0.12,
        ]
        for i, v in enumerate(expected_values):
            cnode = self.cubex.get_cnode(i)
            values = metric_values.cnode_values(cnode)
            self.assertAlmostEqual(v, values[0], 2)

    def test_values_time2(self):
        metric = self.cubex.get_metric_by_name('time')
        metric_values = self.cubex.get_metric_values(metric, cache=False)
        expected_values = [
            74.05,
            74.05,
            60.00,
            10.0, 20.0, 30.0,
            12.00,
            2.0, 4.0, 6.0,
            1.80,
            0.3, 0.6, 0.9,
            0.24,
            0.04, 0.08, 0.12,
        ]

        print(metric_values.values)

        for i, v in enumerate(expected_values):
            cnode = self.cubex.get_cnode(i)
            values = metric_values.cnode_values(cnode)
            self.assertAlmostEqual(v, values[0], 2)

    def test_values_time_exclusive(self):
        metric = self.cubex.get_metric_by_name('time')
        metric_values = self.cubex.get_metric_values(metric, cache=False)
        expected_values = [
            74.05,
            74.05,
            60.00,
            10.0, 20.0, 30.0,
            12.00,
            2.0, 4.0, 6.0,
            1.80,
            0.3, 0.6, 0.9,
            0.24,
            0.04, 0.08, 0.12,
        ]
        for i, v in enumerate(expected_values):
            cnode = self.cubex.get_cnode(i)
            values = metric_values.cnode_values(cnode)
            self.assertAlmostEqual(v, values[0], 2)


class TestCallTree(unittest.TestCase):

    def test_bytes_recieved_problematic_case(self):
        cubex_file_path = Path("../data/time.p4.n2000.x1.r0/profile.cubex").resolve()
        with CubexParser(cubex_file_path) as parsed:
            root_cnodes = parsed.get_root_cnodes()
            callpaths = self._make_callpath_mapping(root_cnodes)
            cube_metric = parsed.get_metric_by_name('bytes_received')
            metric_values = parsed.get_metric_values(metric=cube_metric, cache=False)
            last_mpi_recv = list(metric_values.cnode_indices.keys())[-1]
            # self.assertEqual(last_mpi_recv, 45)
            cnode = parsed.get_cnode(45)
            print(cnode)

    def test_bytes_sent(self):
        cubex_file_path = Path("../data/time.p4.n2000.x1.r0/profile.cubex").resolve()
        with CubexParser(cubex_file_path) as parsed:
            root_cnodes = parsed.get_root_cnodes()
            callpaths, _ = self._make_callpath_mapping(root_cnodes)
            cube_metric = parsed.get_metric_by_name('bytes_sent')
            try:
                metric_values = parsed.get_metric_values(metric=cube_metric, cache=False)
                expected_cnode_ids = [10, 13, 16, 19, 22, 25, 28, 31, 34, 38]
                self.assertListEqual(expected_cnode_ids, list(metric_values.cnode_indices.keys()))
                for cnode_id in metric_values.cnode_indices:
                    cnode = parsed.get_cnode(cnode_id)
                    # self.assertEqual(sorted_ids[cnode_id], cnode_id)
                    callpath = callpaths[cnode_id]
                    self.assertTrue(callpath.endswith(cnode.region.name))
            except MissingMetricError:
                print("Missing metric for", cube_metric.name)

    def test_bytes_recieved(self):
        cubex_file_path = Path("../data/time.p4.n2000.x1.r0/profile.cubex").resolve()
        with CubexParser(cubex_file_path) as parsed:
            root_cnodes = parsed.get_root_cnodes()
            callpaths, _ = self._make_callpath_mapping(root_cnodes)
            cube_metric = parsed.get_metric_by_name('bytes_received')
            try:
                metric_values = parsed.get_metric_values(metric=cube_metric, cache=False)
                expected_cnode_ids = [10, 13, 16, 19, 22, 25, 28, 31, 44, 45]
                self.assertListEqual(expected_cnode_ids, list(metric_values.cnode_indices.keys()))
                for cnode_id in metric_values.cnode_indices:
                    cnode = parsed.get_cnode(cnode_id)
                    # self.assertEqual(sorted_ids[cnode_id], cnode_id)
                    callpath = callpaths[cnode_id]
                    self.assertTrue(callpath.endswith(cnode.region.name))
            except MissingMetricError:
                print("Missing metric for", cube_metric.name)

    def _make_callpath_mapping(self, cnodes):

        sort_callpaths_id = [0]  # Ensures that the callpath ID is compatible for the next steps
        callpaths = {}

        def walk_tree(parent_cnode, parent_name):
            for cnode in parent_cnode.get_children():
                name = cnode.region.name
                path_name = '->'.join((parent_name, name))
                callpath = path_name
                callpaths[cnode.id] = callpath
                sort_callpaths_id.append(cnode.id)
                walk_tree(cnode, path_name)

        for root_cnode in cnodes:
            name = root_cnode.region.name
            callpath = name
            callpaths[root_cnode.id] = callpath
            walk_tree(root_cnode, name)

        return callpaths, sort_callpaths_id


if __name__ == '__main__':
    unittest.main()
