import unittest
from pathlib import Path
from unittest import SkipTest

from pycubexr import CubexParser

DEEP_ENUMERATION = dict(
    [(18, 18), (55, 55), (36, 36), (52, 52), (35, 35), (82, 82), (58, 58), (41, 41), (32, 32), (6, 6), (84, 84),
     (11, 11), (12, 12), (34, 34), (42, 42), (46, 46), (13, 13), (20, 20), (77, 77), (59, 59), (63, 63), (31, 31),
     (23, 23), (24, 24), (57, 57), (79, 79), (21, 21), (10, 10), (72, 72), (40, 40), (73, 73), (27, 27), (2, 2),
     (75, 75), (56, 56), (68, 68), (81, 81), (16, 16), (80, 80), (25, 25), (37, 37), (86, 86), (61, 61), (50, 50),
     (64, 64), (0, 0), (74, 74), (29, 29), (53, 53), (30, 30), (51, 51), (26, 26), (71, 71), (33, 33), (8, 8),
     (85, 85), (19, 19), (5, 5), (47, 47), (3, 3), (38, 38), (44, 44), (49, 49), (65, 65), (43, 43), (88, 88),
     (87, 87), (45, 45), (4, 4), (7, 7), (69, 69), (1, 1), (70, 70), (39, 39), (14, 14), (17, 17), (15, 15),
     (76, 76), (60, 60), (22, 22), (67, 67), (62, 62), (66, 66), (83, 83), (48, 48), (28, 28), (9, 9), (54, 54),
     (78, 78), ])

WIDE_ENUMERATION = dict(
    [(18, 32), (55, 74), (36, 43), (52, 58), (35, 49), (82, 86), (58, 76), (41, 51), (32, 41), (6, 25), (84, 82),
     (11, 6), (12, 7), (34, 42), (46, 54), (42, 61), (13, 8), (20, 34), (77, 80), (59, 67), (63, 70), (31, 40),
     (23, 44), (24, 45), (57, 66), (79, 81), (21, 27), (10, 5), (72, 13), (40, 60), (73, 14), (27, 37), (2, 21),
     (75, 16), (68, 73), (56, 75), (81, 85), (16, 26), (80, 84), (86, 18), (37, 28), (25, 36), (61, 68), (50, 57),
     (64, 71), (0, 0), (74, 15), (29, 38), (53, 29), (30, 39), (51, 64), (71, 12), (26, 46), (33, 48), (8, 3),
     (85, 88), (19, 33), (5, 24), (47, 55), (3, 22), (38, 50), (44, 62), (49, 63), (65, 78), (43, 52), (88, 20),
     (87, 19), (45, 53), (4, 23), (7, 2), (69, 30), (1, 1), (70, 11), (39, 59), (14, 9), (17, 31), (15, 10),
     (76, 17), (60, 77), (22, 35), (67, 79), (62, 69), (66, 72), (83, 87), (48, 56), (28, 47), (9, 4), (54, 65),
     (78, 83), ])


class TestEnumeration(unittest.TestCase):
    cubex: CubexParser = None

    @classmethod
    def setUpClass(cls) -> None:
        try:
            cubex_file_path = Path("../data/cube_samples/summary.cubex").resolve()
            cls.cubex = CubexParser(cubex_file_path).__enter__()
        except FileNotFoundError as err:
            raise SkipTest("Required test file was not found.") from err

    @classmethod
    def tearDownClass(cls) -> None:
        cls.cubex.__exit__(None, None, None)

    def get_enumeration_for_metric(self, name):
        metric = self.cubex.get_metric_by_name(name)
        return metric.tree_enumeration

    def test_time(self):
        enumeration = self.get_enumeration_for_metric('time')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_execution(self):
        enumeration = self.get_enumeration_for_metric('execution')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi(self):
        enumeration = self.get_enumeration_for_metric('mpi')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_synchronization(self):
        enumeration = self.get_enumeration_for_metric('mpi_synchronization')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_sync_collective(self):
        enumeration = self.get_enumeration_for_metric('mpi_sync_collective')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_rma_synchronization(self):
        enumeration = self.get_enumeration_for_metric('mpi_rma_synchronization')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_rma_sync_active(self):
        enumeration = self.get_enumeration_for_metric('mpi_rma_sync_active')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_rma_sync_passive(self):
        enumeration = self.get_enumeration_for_metric('mpi_rma_sync_passive')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_communication(self):
        enumeration = self.get_enumeration_for_metric('mpi_communication')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_point2point(self):
        enumeration = self.get_enumeration_for_metric('mpi_point2point')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_collective(self):
        enumeration = self.get_enumeration_for_metric('mpi_collective')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_rma_communication(self):
        enumeration = self.get_enumeration_for_metric('mpi_rma_communication')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_io(self):
        enumeration = self.get_enumeration_for_metric('mpi_io')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_io_collective(self):
        enumeration = self.get_enumeration_for_metric('mpi_io_collective')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_init_exit(self):
        enumeration = self.get_enumeration_for_metric('mpi_init_exit')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_omp_time(self):
        enumeration = self.get_enumeration_for_metric('omp_time')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_omp_flush(self):
        enumeration = self.get_enumeration_for_metric('omp_flush')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_omp_management(self):
        enumeration = self.get_enumeration_for_metric('omp_management')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_omp_synchronization(self):
        enumeration = self.get_enumeration_for_metric('omp_synchronization')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_omp_barrier(self):
        enumeration = self.get_enumeration_for_metric('omp_barrier')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_omp_ebarrier(self):
        enumeration = self.get_enumeration_for_metric('omp_ebarrier')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_omp_ibarrier(self):
        enumeration = self.get_enumeration_for_metric('omp_ibarrier')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_omp_critical(self):
        enumeration = self.get_enumeration_for_metric('omp_critical')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_omp_lock_api(self):
        enumeration = self.get_enumeration_for_metric('omp_lock_api')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_omp_ordered(self):
        enumeration = self.get_enumeration_for_metric('omp_ordered')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_opencl_time(self):
        enumeration = self.get_enumeration_for_metric('opencl_time')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_opencl_host(self):
        enumeration = self.get_enumeration_for_metric('opencl_host')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_opencl_setup(self):
        enumeration = self.get_enumeration_for_metric('opencl_setup')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_opencl_comm(self):
        enumeration = self.get_enumeration_for_metric('opencl_comm')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_opencl_sync(self):
        enumeration = self.get_enumeration_for_metric('opencl_sync')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_opencl_kernel_launches(self):
        enumeration = self.get_enumeration_for_metric('opencl_kernel_launches')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_opencl_device(self):
        enumeration = self.get_enumeration_for_metric('opencl_device')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_opencl_kernel_executions(self):
        enumeration = self.get_enumeration_for_metric('opencl_kernel_executions')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_pthread_time(self):
        enumeration = self.get_enumeration_for_metric('pthread_time')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_pthread_management(self):
        enumeration = self.get_enumeration_for_metric('pthread_management')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_pthread_synchronization(self):
        enumeration = self.get_enumeration_for_metric('pthread_synchronization')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_pthread_mutex_api(self):
        enumeration = self.get_enumeration_for_metric('pthread_mutex_api')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_pthread_cond_api(self):
        enumeration = self.get_enumeration_for_metric('pthread_cond_api')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_overhead(self):
        enumeration = self.get_enumeration_for_metric('overhead')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_omp_idle_threads(self):
        enumeration = self.get_enumeration_for_metric('omp_idle_threads')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_omp_limited_parallelism(self):
        enumeration = self.get_enumeration_for_metric('omp_limited_parallelism')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_visits(self):
        enumeration = self.get_enumeration_for_metric('visits')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_syncs(self):
        enumeration = self.get_enumeration_for_metric('syncs')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_syncs_rma(self):
        enumeration = self.get_enumeration_for_metric('syncs_rma')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_syncs_fence(self):
        enumeration = self.get_enumeration_for_metric('syncs_fence')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_syncs_gats(self):
        enumeration = self.get_enumeration_for_metric('syncs_gats')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_syncs_gats_access(self):
        enumeration = self.get_enumeration_for_metric('syncs_gats_access')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_syncs_gats_exposure(self):
        enumeration = self.get_enumeration_for_metric('syncs_gats_exposure')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_syncs_locks(self):
        enumeration = self.get_enumeration_for_metric('syncs_locks')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_comms(self):
        enumeration = self.get_enumeration_for_metric('comms')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_comms_rma(self):
        enumeration = self.get_enumeration_for_metric('comms_rma')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_comms_rma_puts(self):
        enumeration = self.get_enumeration_for_metric('comms_rma_puts')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_comms_rma_gets(self):
        enumeration = self.get_enumeration_for_metric('comms_rma_gets')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_bytes(self):
        enumeration = self.get_enumeration_for_metric('bytes')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_bytes_p2p(self):
        enumeration = self.get_enumeration_for_metric('bytes_p2p')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_bytes_sent_p2p(self):
        enumeration = self.get_enumeration_for_metric('bytes_sent_p2p')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_bytes_received_p2p(self):
        enumeration = self.get_enumeration_for_metric('bytes_received_p2p')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_bytes_coll(self):
        enumeration = self.get_enumeration_for_metric('bytes_coll')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_bytes_sent_coll(self):
        enumeration = self.get_enumeration_for_metric('bytes_sent_coll')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_bytes_received_coll(self):
        enumeration = self.get_enumeration_for_metric('bytes_received_coll')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_bytes_rma(self):
        enumeration = self.get_enumeration_for_metric('bytes_rma')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_bytes_put(self):
        enumeration = self.get_enumeration_for_metric('bytes_put')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_bytes_get(self):
        enumeration = self.get_enumeration_for_metric('bytes_get')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_file_ops(self):
        enumeration = self.get_enumeration_for_metric('mpi_file_ops')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_file_iops(self):
        enumeration = self.get_enumeration_for_metric('mpi_file_iops')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_file_irops(self):
        enumeration = self.get_enumeration_for_metric('mpi_file_irops')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_file_iwops(self):
        enumeration = self.get_enumeration_for_metric('mpi_file_iwops')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_file_cops(self):
        enumeration = self.get_enumeration_for_metric('mpi_file_cops')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_file_crops(self):
        enumeration = self.get_enumeration_for_metric('mpi_file_crops')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_mpi_file_cwops(self):
        enumeration = self.get_enumeration_for_metric('mpi_file_cwops')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_imbalance(self):
        enumeration = self.get_enumeration_for_metric('imbalance')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_imbalance_above(self):
        enumeration = self.get_enumeration_for_metric('imbalance_above')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_imbalance_above_single(self):
        enumeration = self.get_enumeration_for_metric('imbalance_above_single')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_imbalance_below(self):
        enumeration = self.get_enumeration_for_metric('imbalance_below')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_imbalance_below_bypass(self):
        enumeration = self.get_enumeration_for_metric('imbalance_below_bypass')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_imbalance_below_singularity(self):
        enumeration = self.get_enumeration_for_metric('imbalance_below_singularity')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_min_time(self):
        enumeration = self.get_enumeration_for_metric('min_time')
        self.assertDictEqual(DEEP_ENUMERATION, enumeration)

    def test_max_time(self):
        enumeration = self.get_enumeration_for_metric('max_time')
        self.assertDictEqual(DEEP_ENUMERATION, enumeration)

    def test_task_migration_loss(self):
        enumeration = self.get_enumeration_for_metric('task_migration_loss')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)

    def test_task_migration_win(self):
        enumeration = self.get_enumeration_for_metric('task_migration_win')
        self.assertDictEqual(WIDE_ENUMERATION, enumeration)


if __name__ == '__main__':
    unittest.main()
