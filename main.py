from glob import glob

from pycubex_parser import CubexTarParser
from pycubex_parser.utils.exceptions import MissingMetricError


def main():
    for folder in sorted(glob('assets/*.r1')):
        print('-' * 99)
        print(folder)

        profile = f'{folder}/profile.cubex'

        with CubexTarParser(profile) as parsed:
            parsed.anchor_parser.print_calltree()

            for metric in parsed.anchor_parser.metrics:
                try:
                    metric_values = parsed.get_metric_values(metric=metric)
                    cnode = parsed.anchor_parser.get_cnode(metric_values.cnode_indices[0])
                    cnode_values = metric_values.cnode_values(cnode.id)[:5]
                    region = parsed.anchor_parser.get_region(cnode)
                    print('\t' + '-' * 100)
                    print(f'\tRegion: {region.name}\n\tMetric: {metric.name}\n\tMetricValues: {cnode_values})')
                except MissingMetricError as e:
                    pass


if __name__ == '__main__':
    main()
