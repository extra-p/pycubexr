import os
import xml.etree.ElementTree as ElementTree
from glob import glob

from cubex_lib.parsers.parser import CubexAnchorXMLParser, CubexTarParser

FOLDER = 'assets/kripke.p32768.d12.g160.r1/unpacked'


def main():
    for folder in sorted(glob('assets/*.r1')):
        print('-' * 99)
        print(folder)

        profile = f'{folder}/profile.cubex'

        parsed = CubexTarParser(profile)

        for metric in parsed.anchor_parser.metrics:
            try:
                metric_values = parsed.get_metric_values(
                    metric=metric
                )
                cnode = metric_values.cnode_indices[0]
                region = parsed.anchor_parser.get_region(parsed.anchor_parser.get_cnode(cnode))
                print('\t' + '-' * 100)
                print(f'\tRegion: {region.name}\n\tMetric: {metric.name}\n\tMetricValues: {metric_values.values[:10]})')
            except Exception as e:
                if str(e).startswith('The cubex file does NOT contain values'):
                    continue
                print(f'Error extracting metric ({metric.name}): {e}. Ignoring')


if __name__ == '__main__':
    main()
