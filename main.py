import xml.etree.ElementTree as ET

from cubex_lib.parsers.parser import CubexAnchorXMLParser

FOLDER = 'assets/fastest.p16.size131072.r1/unpacked'
ANCHOR_FILE = f'{FOLDER}/anchor.xml'


def main():
    parsed = parse_anchor_file()
    print(
        [x.id for x in parsed.system_tree_nodes[0].all_locations()]
    )

    metric = parsed.get_metric_by_name('time')

    index_filename = f'{FOLDER}/{metric.id}.index'
    data_filename = f'{FOLDER}/{metric.id}.data'

    with open(index_filename, 'rb') as index_file, open(data_filename, 'rb') as data_file:
        out = parsed.get_metric_values(metric, index_file=index_file, data_file=data_file)
        print(out)


def parse_anchor_file(file=ANCHOR_FILE):
    root = ET.parse(file).getroot()

    parsed = CubexAnchorXMLParser(root)
    assert len(parsed.cnodes) == 1
    assert len(parsed.system_tree_nodes) == 1
    return parsed


if __name__ == '__main__':
    main()
