from xml.etree.ElementTree import Element as XMLNode

from cubex_lib.classes import CNode, Location, LocationGroup, Metric, Region, SystemTreeNode


class CubexXMLParsers(object):

    @staticmethod
    def parse_metric(xml_node: XMLNode):
        return Metric(
            name=xml_node.find('uniq_name').text,
            _id=int(xml_node.get('id')),
            display_name=xml_node.find('disp_name').text,
            description=xml_node.find('descr').text,
            metric_type=xml_node.get('type'),
            data_type=xml_node.find('dtype').text,
            units=xml_node.find('uom').text,
            url=xml_node.find('url').text
        )

    @staticmethod
    def parse_metrics(root: XMLNode):
        metrics = root.find('metrics').findall('metric')
        return [CubexXMLParsers.parse_metric(metric_xml_node) for metric_xml_node in metrics]

    @staticmethod
    def parse_region(xml_node: XMLNode):
        return Region(
            _id=int(xml_node.get('id')),
            begin=int(xml_node.get('begin')),
            end=int(xml_node.get('end')),
            name=xml_node.find('name').text,
            mangled_name=xml_node.find('mangled_name').text,
            paradigm=xml_node.find('paradigm').text,
            role=xml_node.find('role').text,
            url=xml_node.find('url').text,
            descr=xml_node.find('descr').text,
        )

    @staticmethod
    def parse_regions(root: XMLNode):
        regions = root.find('program').findall('region')
        return [CubexXMLParsers.parse_region(xml_node) for xml_node in regions]

    @staticmethod
    def parse_attrs(root: XMLNode):
        return {node.get('key'): node.get('value') for node in root.findall('attr')}

    @staticmethod
    def parse_cnode(xml_node: XMLNode):
        cnode = CNode(
            _id=int(xml_node.get('id')),
            callee_region_id=int(xml_node.get('calleeId'))
        )
        for cnode_xml_child in xml_node.findall('cnode'):
            cnode_child = CubexXMLParsers.parse_cnode(cnode_xml_child)
            cnode.add_child(cnode_child)
        return cnode

    @staticmethod
    def parse_cnodes(root: XMLNode):
        cnodes = root.find('program').findall('cnode')
        return [CubexXMLParsers.parse_cnode(cnode) for cnode in cnodes]

    @staticmethod
    def parse_location(xml_node: XMLNode):
        return Location(
            _id=int(xml_node.get('Id')),
            name=xml_node.find('name').text,
            rank=xml_node.find('rank').text,
            _type=xml_node.find('type').text
        )

    @staticmethod
    def parse_location_group(xml_node: XMLNode):
        location_group = LocationGroup(
            _id=int(xml_node.get('Id')),
            name=xml_node.find('name').text,
            rank=xml_node.find('rank').text,
            _type=xml_node.find('type').text
        )

        for xml_child_node in xml_node.findall('locationgroup'):
            location_group.add_location_group(CubexXMLParsers.parse_location_group(xml_child_node))

        for xml_child_node in xml_node.findall('location'):
            location_group.add_location(CubexXMLParsers.parse_location(xml_child_node))

        return location_group

    @staticmethod
    def parse_system_tree_node(xml_node: XMLNode):
        system_tree_node = SystemTreeNode(
            _id=int(xml_node.get('Id')),
            clazz=xml_node.get('class'),
            name=xml_node.find('name').text,
            attrs={x.get('key'): x.get('value') for x in xml_node.findall('attr')}
        )

        for xml_child_node in xml_node.findall('systemtreenode'):
            system_tree_node.add_system_tree_node_child(CubexXMLParsers.parse_system_tree_node(xml_child_node))

        for xml_child_node in xml_node.findall('locationgroup'):
            system_tree_node.add_location_group(CubexXMLParsers.parse_location_group(xml_child_node))

        return system_tree_node

    @staticmethod
    def parse_system_tree_nodes(root: XMLNode):
        system_tree_node_xml_nodes = root.find('system').findall('systemtreenode')
        return [CubexXMLParsers.parse_system_tree_node(xml_node) for xml_node in system_tree_node_xml_nodes]
