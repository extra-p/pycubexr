import os
import xml.etree.ElementTree as ET

from cubex_lib.parsers.parser import CubexAnchorXMLParser

FOLDER = 'assets/kripke.p32768.d12.g160.r1/unpacked'
ANCHOR_FILE = f'{FOLDER}/anchor.xml'


def main():
    parsed = parse_anchor_file()
    for metric in parsed.metrics:
        index_filename = f'{FOLDER}/{metric.id}.index'
        data_filename = f'{FOLDER}/{metric.id}.data'

        if not os.path.exists(index_filename) or not os.path.exists(data_filename):
            continue

        with open(index_filename, 'rb') as index_file, open(data_filename, 'rb') as data_file:
            metric_values = parsed.get_metric_values(
                metric=metric,
                index_file=index_file,
                data_file=data_file
            )
            print(f'Metric: {metric.name}\n\tMetricValues: {metric_values.values[:10]})')


def parse_anchor_file(file=ANCHOR_FILE):
    root = ET.parse(file).getroot()

    parsed = CubexAnchorXMLParser(root)
    assert len(parsed.cnodes) == 1
    assert len(parsed.system_tree_nodes) == 1
    return parsed


if __name__ == '__main__':
    main()
