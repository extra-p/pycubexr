from xml.etree.ElementTree import Element as XMLNode, ElementTree

from pycubexr.classes import CNode, Location, LocationGroup, Metric, Region, SystemTreeNode


def parse_metric(xml_node: XMLNode):
    return Metric(
        name=xml_node.findtext('uniq_name'),
        _id=int(xml_node.get('id')),
        display_name=xml_node.findtext('disp_name'),
        description=xml_node.findtext('descr'),
        metric_type=xml_node.get('type'),
        data_type=xml_node.findtext('dtype'),
        units=xml_node.findtext('uom'),
        url=xml_node.findtext('url'),
        childs=parse_metrics(xml_node)
    )


def parse_metrics(root: XMLNode):
    if isinstance(root, ElementTree):
        root = root.find('metrics')
    return [
        parse_metric(metric_xml_node) for metric_xml_node
        in root.findall('metric')
    ]


def parse_region(xml_node: XMLNode):
    return Region(
        _id=int(xml_node.get('id')),
        begin=int(xml_node.get('begin')),
        end=int(xml_node.get('end')),
        name=xml_node.findtext('name'),
        mangled_name=xml_node.findtext('mangled_name'),
        paradigm=xml_node.findtext('paradigm'),
        role=xml_node.findtext('role'),
        url=xml_node.findtext('url'),
        descr=xml_node.findtext('descr'),
        mod=xml_node.get("mod"),
    )


def parse_regions(root: XMLNode):
    return [
        parse_region(xml_node) for xml_node
        in root.find('program').findall('region')
    ]


def parse_attrs(root: XMLNode):
    return {
        node.get('key'): node.get('value') for node
        in root.findall('attr')
    }


def parse_cnode(xml_node: XMLNode):
    cnode = CNode(
        _id=int(xml_node.get('id')),
        callee_region_id=int(xml_node.get('calleeId'))
    )
    for cnode_xml_child in xml_node.findall('cnode'):
        cnode_child = parse_cnode(cnode_xml_child)
        cnode.add_child(cnode_child)
    for parameter_xml in xml_node.findall('parameter'):
        partype = parameter_xml.get('partype')
        parkey = parameter_xml.get('parkey')
        parvalue = parameter_xml.get('parvalue')
        if partype == 'numeric':
            try:
                parvalue = int(parvalue)
            except ValueError:
                parvalue = float(parvalue)
        elif partype == "string":
            pass
        cnode.parameters[parkey] = parvalue
    return cnode


def parse_cnodes(root: XMLNode):
    return [
        parse_cnode(cnode) for cnode
        in root.find('program').findall('cnode')
    ]


def parse_location(xml_node: XMLNode):
    return Location(
        _id=int(xml_node.get('Id')),
        name=xml_node.findtext('name'),
        rank=xml_node.findtext('rank'),
        _type=xml_node.findtext('type')
    )


def parse_location_group(xml_node: XMLNode):
    location_group = LocationGroup(
        _id=int(xml_node.get('Id')),
        name=xml_node.findtext('name'),
        rank=xml_node.findtext('rank'),
        _type=xml_node.findtext('type')
    )

    for xml_child_node in xml_node.findall('locationgroup'):
        location_group.add_location_group(parse_location_group(xml_child_node))

    for xml_child_node in xml_node.findall('location'):
        location_group.add_location(parse_location(xml_child_node))

    return location_group


def parse_system_tree_node(xml_node: XMLNode):
    system_tree_node = SystemTreeNode(
        _id=int(xml_node.get('Id')),
        _class=xml_node.get('class'),
        name=xml_node.findtext('name'),
        attrs={x.get('key'): x.get('value') for x in xml_node.findall('attr')}
    )

    for xml_child_node in xml_node.findall('systemtreenode'):
        system_tree_node.add_system_tree_node_child(parse_system_tree_node(xml_child_node))

    for xml_child_node in xml_node.findall('locationgroup'):
        system_tree_node.add_location_group(parse_location_group(xml_child_node))

    return system_tree_node


def parse_system_tree_nodes(root: XMLNode):
    return [
        parse_system_tree_node(xml_node) for xml_node
        in root.find('system').findall('systemtreenode')
    ]
