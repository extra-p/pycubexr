import unittest
from collections import defaultdict

import numpy as np

from pycubexr.utils.exceptions import MissingMetricError

from pycubexr import CubexParser


class TestExtraPUseCase(unittest.TestCase):

    def test_weak_exclusive(self):
        self.execute()

    def test_strong_exclusive(self):
        self.execute(scaling_type='strong')

    def execute(self, scaling_type='weak', use_inclusive_measurements=False):
        aggregated_values = defaultdict(list)
        for i in range(5):
            with CubexParser('../data/miniFE/profile.cubex') as parsed:
                # iterate over all metrics
                for cube_metric in parsed.get_metrics():
                    try:
                        metric_values = parsed.get_metric_values(metric=cube_metric, cache=False)
                        # create the metrics
                        metric = cube_metric.name

                        for cnode_id in metric_values.cnode_indices:
                            cnode = parsed.get_cnode(cnode_id)
                            callpath = cnode.region.name
                            # NOTE: here we can use clustering algorithm to select only certain node level values
                            # create the measurements
                            cnode_values = metric_values.cnode_values(cnode,
                                                                      convert_to_exclusive=not use_inclusive_measurements,
                                                                      convert_to_inclusive=use_inclusive_measurements)

                            # in case of weak scaling calculate mean and median over all mpi process values
                            if scaling_type == "weak":
                                # do NOT use generator it is slower
                                if isinstance(cnode_values, np.ndarray):
                                    aggregated_values[(callpath, metric)].append(cnode_values)
                                else:
                                    try:
                                        aggregated_values[(callpath, metric)].append(cnode_values.astype(float))
                                    except AttributeError as e:
                                        print(e)
                                        print(cnode_values)
                                # else:
                                #     aggregated_values[(callpath, metric)].extend(map(float, cnode_values))

                                # in case of strong scaling calculate the sum over all mpi process values
                            elif scaling_type == "strong":
                                aggregated_values[(callpath, metric)].append(cnode_values.sum().astype(float))

                    # Take care of missing metrics
                    except MissingMetricError as e:  # @UnusedVariable
                        pass


if __name__ == '__main__':
    unittest.main()
