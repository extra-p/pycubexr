from glob import glob

from pycube import CubexParser
from pycube.utils.exceptions import MissingMetricError

#"data/blast.p64.r1/profile.cubex"
#'assets/*.r1'

def main():
    for folder in sorted(glob('../data/one_parameter')):
        print('-' * 99)
        print(folder)

        profile = f'{folder}/profile.cubex'

        with CubexParser(profile) as parsed:
            parsed.print_calltree()

            # extracting all the metrics
            # should extract only the ones we can actually model
            # or offer the user to choose them...
            for metric in parsed.get_metrics():
                try:
                    metric_values = parsed.get_metric_values(metric=metric)
                    # with the cnode_indices I can manipulate the region that is chosen
                    # should put for here to extract all of them
                    cnode = parsed.get_cnode(metric_values.cnode_indices[0])
                    #debug
                    #print(metric_values.cnode_indices)
                    #print("node values:",metric_values.cnode_values(cnode.id))
                    #print("number node values:",len(metric_values.cnode_values(cnode.id)))

                    # the more processes the more values per node, like this shows only 5 of them
                    # here we will do some magic with selecting only certain values based on that clustering algorithm
                    cnode_values = metric_values.cnode_values(cnode.id)[:5]
                    region = parsed.get_region(cnode)
                    print('\t' + '-' * 100)
                    print(f'\tRegion: {region.name}\n\tMetric: {metric.name}\n\tMetricValues: {cnode_values})')
                except MissingMetricError as e:
                    # Ignore missing metrics
                    pass


if __name__ == '__main__':
    main()
