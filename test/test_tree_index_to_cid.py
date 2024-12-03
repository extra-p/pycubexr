import unittest
from pathlib import Path

from pycubexr import CubexParser
from pycubexr.classes.metric import MetricType
from pycubexr.utils.exceptions import MissingMetricError


class AbstractTestcase:
    class Mapping(unittest.TestCase):
        expected_mapping_visits: list
        expected_mapping_time: list
        path: str = None

        @classmethod
        def setUpClass(cls) -> None:
            if cls.path is None:
                raise unittest.SkipTest
            cubex_file_path = Path(cls.path).resolve()
            cls.cubex = CubexParser(cubex_file_path).__enter__()

        @classmethod
        def tearDownClass(cls) -> None:
            cls.cubex.__exit__(None, None, None)

        def test_visits(self):
            metric = self.cubex.get_metric_by_name('visits')
            self.assertEqual(MetricType.EXCLUSIVE, metric.metric_type)
            self.perform_test(metric, self.expected_mapping_visits)

        def test_time(self):
            metric = self.cubex.get_metric_by_name('time')
            self.assertEqual(MetricType.INCLUSIVE, metric.metric_type)
            self.perform_test(metric, self.expected_mapping_time)

        def test_other_metrics(self):
            for metric in self.cubex.get_metrics():
                if metric.metric_type == MetricType.EXCLUSIVE:
                    expected_mapping = self.expected_mapping_visits
                elif metric.metric_type == MetricType.INCLUSIVE:
                    expected_mapping = self.expected_mapping_time
                else:
                    self.fail("Unknown metric type")

                tree_index_to_cid_map = metric.tree_index_to_cid_map
                try:
                    cnode_indices = self.cubex.get_metric_values(metric, False).cnode_indices
                except MissingMetricError:
                    return
                for index, cid, cname in expected_mapping:
                    self.assertEqual(cid, tree_index_to_cid_map[index])
                    if cid in cnode_indices:
                        self.assertEqual(index, cnode_indices[cid], msg=str((metric.name, index, cid, cname)))
                    self.assertEqual(cname, self.cubex.get_cnode(cid).region.mangled_name)

        def perform_test(self, metric, expected_mapping):
            tree_index_to_cid_map = metric.tree_index_to_cid_map
            try:
                cnode_indices = self.cubex.get_metric_values(metric, False).cnode_indices
            except MissingMetricError:
                return
            self.assertEqual(len(cnode_indices), len(expected_mapping))
            for index, cid, cname in expected_mapping:
                self.assertEqual(cid, tree_index_to_cid_map[index])
                # the following is only true for metrics that have data for all call paths
                self.assertEqual(index, cnode_indices[cid], msg=str((metric.name, index, cid, cname)))
                self.assertEqual(cname, self.cubex.get_cnode(cid).region.mangled_name)


class TestSimpleCallTree(AbstractTestcase.Mapping):
    path = "../data/call_tree_test/call_tree_test.cubex"
    expected_mapping_visits = [
        # index,cnode_id,cnode_mangled_name
        (0, 0, "cube_test_file/test.x"),
        (1, 1, "main"),
        (2, 2, "a"),
        (3, 3, "a1"),
        (4, 4, "a2"),
        (5, 5, "a3"),
        (6, 6, "b"),
        (7, 7, "b1"),
        (8, 8, "b2"),
        (9, 9, "b3"),
        (10, 10, "c"),
        (11, 11, "c1"),
        (12, 12, "c2"),
        (13, 13, "c3"),
        (14, 14, "d"),
        (15, 15, "d1"),
        (16, 16, "d2"),
        (17, 17, "d3"),
    ]
    expected_mapping_time = [
        # index,cnode_id,cnode_mangled_name
        (0, 0, "cube_test_file/test.x"),
        (1, 1, "main"),
        (2, 2, "a"),
        (3, 6, "b"),
        (4, 10, "c"),
        (5, 14, "d"),
        (6, 3, "a1"),
        (7, 4, "a2"),
        (8, 5, "a3"),
        (9, 7, "b1"),
        (10, 8, "b2"),
        (11, 9, "b3"),
        (12, 11, "c1"),
        (13, 12, "c2"),
        (14, 13, "c3"),
        (15, 15, "d1"),
        (16, 16, "d2"),
        (17, 17, "d3"),
    ]


class TestProblematicCallTree(AbstractTestcase.Mapping):
    path = "../data/time.p4.n2000.x1.r0/profile.cubex"
    expected_mapping_visits = [
        # index,cnode_id,cnode_mangled_name
        (0, 0, "/work/home/ga42biko/new_codes/Benchmark_V2/A8/Test_A/bg_time -n 2000 -x 1"),
        (1, 1, "main"),
        (2, 2, "MPI_Init"),
        (3, 3, "MPI_Comm_rank"),
        (4, 4, "MPI_Comm_size"),
        (5, 5, "_Z7MODEL_1mmii"),
        (6, 6, "_ZN2bg6VectorIdEC2Em"),
        (7, 7, "_ZN2bg10DataStructIdEC2Ev"),
        (8, 8, "_ZN2bg6VectorIdEclEi"),
        (9, 9, "_ZN2bg8function3F_0IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (10, 10, "MPI_Bcast"),
        (11, 11, "_ZN2bg6VectorIdEclEi"),
        (12, 12, "_ZN2bg8function3F_1IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (13, 13, "MPI_Scatter"),
        (14, 14, "_ZN2bg6VectorIdEclEi"),
        (15, 15, "_ZN2bg8function3F_2IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (16, 16, "MPI_Allgather"),
        (17, 17, "_ZN2bg6VectorIdEclEi"),
        (18, 18, "_ZN2bg8function3F_3IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (19, 19, "MPI_Reduce"),
        (20, 20, "_ZN2bg6VectorIdEclEi"),
        (21, 21, "_ZN2bg8function3F_4IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (22, 22, "MPI_Allreduce"),
        (23, 23, "_ZN2bg6VectorIdEclEi"),
        (24, 24, "_ZN2bg8function3F_5IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (25, 25, "MPI_Bcast"),
        (26, 26, "_ZN2bg6VectorIdEclEi"),
        (27, 27, "_ZN2bg8function3F_6IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (28, 28, "MPI_Scatter"),
        (29, 29, "_ZN2bg6VectorIdEclEi"),
        (30, 30, "_ZN2bg8function3F_7IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (31, 31, "MPI_Gather"),
        (32, 32, "_ZN2bg6VectorIdEclEi"),
        (33, 33, "_ZN2bg8function3F_8IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (34, 34, "MPI_Send"),
        (35, 35, "MPI_Barrier"),
        (36, 36, "_ZN2bg6VectorIdEclEi"),
        (37, 44, "MPI_Recv"),
        (38, 37, "_ZN2bg8function3F_9IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (39, 38, "MPI_Send"),
        (40, 39, "MPI_Barrier"),
        (41, 40, "_ZN2bg6VectorIdEclEi"),
        (42, 45, "MPI_Recv"),
        (43, 41, "_ZN2bg6VectorIdED2Ev"),
        (44, 42, "_ZN2bg10DataStructIdED2Ev"),
        (45, 43, "MPI_Finalize"),
    ]
    expected_mapping_time = [
        # index,cnode_id,cnode_mangled_name
        (0, 0, "/work/home/ga42biko/new_codes/Benchmark_V2/A8/Test_A/bg_time -n 2000 -x 1"),
        (1, 1, "main"),
        (2, 2, "MPI_Init"),
        (3, 3, "MPI_Comm_rank"),
        (4, 4, "MPI_Comm_size"),
        (5, 5, "_Z7MODEL_1mmii"),
        (6, 43, "MPI_Finalize"),
        (7, 6, "_ZN2bg6VectorIdEC2Em"),
        (8, 8, "_ZN2bg6VectorIdEclEi"),
        (9, 9, "_ZN2bg8function3F_0IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (10, 12, "_ZN2bg8function3F_1IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (11, 15, "_ZN2bg8function3F_2IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (12, 18, "_ZN2bg8function3F_3IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (13, 21, "_ZN2bg8function3F_4IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (14, 24, "_ZN2bg8function3F_5IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (15, 27, "_ZN2bg8function3F_6IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (16, 30, "_ZN2bg8function3F_7IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (17, 33, "_ZN2bg8function3F_8IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (18, 37, "_ZN2bg8function3F_9IdEEvmmRNS_6VectorIT_EES5_S5_S5_mmii"),
        (19, 41, "_ZN2bg6VectorIdED2Ev"),
        (20, 7, "_ZN2bg10DataStructIdEC2Ev"),
        (21, 10, "MPI_Bcast"),
        (22, 11, "_ZN2bg6VectorIdEclEi"),
        (23, 13, "MPI_Scatter"),
        (24, 14, "_ZN2bg6VectorIdEclEi"),
        (25, 16, "MPI_Allgather"),
        (26, 17, "_ZN2bg6VectorIdEclEi"),
        (27, 19, "MPI_Reduce"),
        (28, 20, "_ZN2bg6VectorIdEclEi"),
        (29, 22, "MPI_Allreduce"),
        (30, 23, "_ZN2bg6VectorIdEclEi"),
        (31, 25, "MPI_Bcast"),
        (32, 26, "_ZN2bg6VectorIdEclEi"),
        (33, 28, "MPI_Scatter"),
        (34, 29, "_ZN2bg6VectorIdEclEi"),
        (35, 31, "MPI_Gather"),
        (36, 32, "_ZN2bg6VectorIdEclEi"),
        (37, 34, "MPI_Send"),
        (38, 35, "MPI_Barrier"),
        (39, 36, "_ZN2bg6VectorIdEclEi"),
        (40, 44, "MPI_Recv"),
        (41, 38, "MPI_Send"),
        (42, 39, "MPI_Barrier"),
        (43, 40, "_ZN2bg6VectorIdEclEi"),
        (44, 45, "MPI_Recv"),
        (45, 42, "_ZN2bg10DataStructIdED2Ev"),
    ]
    expected_bytes_sent = [
        # tree_index,cnode_id,cnode_mangled_name,file_index
        (10, 10, "MPI_Bcast", 0),
        (13, 13, "MPI_Scatter", 1),
        (16, 16, "MPI_Allgather", 2),
        (19, 19, "MPI_Reduce", 3),
        (22, 22, "MPI_Allreduce", 4),
        (25, 25, "MPI_Bcast", 5),
        (28, 28, "MPI_Scatter", 6),
        (31, 31, "MPI_Gather", 7),
        (34, 34, "MPI_Send", 8),
        (39, 38, "MPI_Send", 9),
    ]

    expected_bytes_received = [
        # tree_index,cnode_id,cnode_mangled_name,file_index
        (10, 10, "MPI_Bcast", 0),
        (13, 13, "MPI_Scatter", 1),
        (16, 16, "MPI_Allgather", 2),
        (19, 19, "MPI_Reduce", 3),
        (22, 22, "MPI_Allreduce", 4),
        (25, 25, "MPI_Bcast", 5),
        (28, 28, "MPI_Scatter", 6),
        (31, 31, "MPI_Gather", 7),
        (37, 44, "MPI_Recv", 8),
        (42, 45, "MPI_Recv", 9),
    ]

    def test_bytes_sent(self):
        metric = self.cubex.get_metric_by_name('bytes_sent')
        self.assertEqual(MetricType.EXCLUSIVE, metric.metric_type)
        tree_index_to_cid_map = metric.tree_index_to_cid_map
        cnode_indices = self.cubex.get_metric_values(metric, False).cnode_indices
        self.assertEqual(len(cnode_indices), len(self.expected_bytes_sent))
        for index, cid, cname, findex in self.expected_bytes_sent:
            self.assertEqual(cid, tree_index_to_cid_map[index])
            self.assertEqual(findex, cnode_indices[cid], msg=str((metric.name, index, cid, cname)))
            self.assertEqual(cname, self.cubex.get_cnode(cid).region.mangled_name)

    def test_bytes_recieved(self):
        metric = self.cubex.get_metric_by_name('bytes_received')
        self.assertEqual(MetricType.EXCLUSIVE, metric.metric_type)
        tree_index_to_cid_map = metric.tree_index_to_cid_map
        cnode_indices = self.cubex.get_metric_values(metric, False).cnode_indices
        self.assertEqual(len(cnode_indices), len(self.expected_bytes_received))
        for index, cid, cname, findex in self.expected_bytes_received:
            self.assertEqual(cid, tree_index_to_cid_map[index])
            self.assertEqual(findex, cnode_indices[cid], msg=str((metric.name, index, cid, cname)))
            self.assertEqual(cname, self.cubex.get_cnode(cid).region.mangled_name)


class TestBlast(AbstractTestcase.Mapping):
    path = "../data/blast.p64.r1/profile.cubex"

    expected_mapping_visits = [
        # index,cnode_id,cnode_mangled_name
        (0, 0, "PARALLEL"),
        (1, 1, "MPI_Init"),
        (2, 2, "MPI_Comm_size"),
        (3, 3, "MPI_Comm_rank"),
        (4, 4, "MPI_Bcast"),
        (5, 5, "MPI_Isend"),
        (6, 6, "MPI_Waitall"),
        (7, 7, "MPI_Allgather"),
        (8, 8, "MPI_Reduce"),
        (9, 9, "MPI_Allreduce"),
        (10, 10, "MPI_Irecv"),
        (11, 11, "MPI_Allgatherv"),
        (12, 12, "ComputeCornerForces"),
        (13, 13, "MPI_Reduce"),
        (14, 14, "main"),
        (15, 15, "MPI_Comm_rank"),
        (16, 16, "MPI_Comm_size"),
        (17, 17, "MPI_Irecv"),
        (18, 18, "MPI_Waitall"),
        (19, 19, "MPI_Isend"),
        (20, 20, "Eval_dv_dt"),
        (21, 21, "MPI_Comm_rank"),
        (22, 22, "MPI_Comm_size"),
        (23, 23, "MPI_Irecv"),
        (24, 24, "MPI_Isend"),
        (25, 25, "MPI_Waitall"),
        (26, 26, "MPI_Allreduce"),
        (27, 27, "ComputeCornerForces"),
        (28, 28, "MPI_Reduce"),
        (29, 29, "MPI_Allreduce"),
        (30, 30, "MPI_Finalize"),
        (31, 31, "MPI_Recv"),
    ]
    expected_mapping_time = [
        # index,cnode_id,cnode_mangled_name
        (0, 0, "PARALLEL"),
        (1, 1, "MPI_Init"),
        (2, 2, "MPI_Comm_size"),
        (3, 3, "MPI_Comm_rank"),
        (4, 4, "MPI_Bcast"),
        (5, 5, "MPI_Isend"),
        (6, 6, "MPI_Waitall"),
        (7, 7, "MPI_Allgather"),
        (8, 8, "MPI_Reduce"),
        (9, 9, "MPI_Allreduce"),
        (10, 10, "MPI_Irecv"),
        (11, 11, "MPI_Allgatherv"),
        (12, 12, "ComputeCornerForces"),
        (13, 14, "main"),
        (14, 30, "MPI_Finalize"),
        (15, 31, "MPI_Recv"),
        (16, 13, "MPI_Reduce"),
        (17, 15, "MPI_Comm_rank"),
        (18, 16, "MPI_Comm_size"),
        (19, 17, "MPI_Irecv"),
        (20, 18, "MPI_Waitall"),
        (21, 19, "MPI_Isend"),
        (22, 20, "Eval_dv_dt"),
        (23, 27, "ComputeCornerForces"),
        (24, 29, "MPI_Allreduce"),
        (25, 21, "MPI_Comm_rank"),
        (26, 22, "MPI_Comm_size"),
        (27, 23, "MPI_Irecv"),
        (28, 24, "MPI_Isend"),
        (29, 25, "MPI_Waitall"),
        (30, 26, "MPI_Allreduce"),
        (31, 28, "MPI_Reduce"),
    ]
