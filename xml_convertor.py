"""
Functions performing XML conversion from one format to another
based on an xml template.
"""
import xml.etree.ElementTree as ET

def convert_xml(input_xml):
    """
    Return XML converted from input_xml to a fromat specified by the template.
    """
    
    input_root = ET.fromstring(input_xml)

    template_tree = ET.parse('template.xml')
    template_root = template_tree.getroot()

    root = ET.Element('InvoiceRegisters')
    fill_template(template_root, root, input_root)

    ET.indent(root)
    return ET.tostring(root)

def fill_template(template, output, input):
    """
    Recursively fill the output element with tags defined in template taking
    values from input.
    """
    for child in template:
        output_element = ET.SubElement(output, child.tag)
        from_id = child.get('from')
        if from_id:
            try:
                output_element.text = input.find(f'.//datapoint/[@schema_id="{from_id}"]').text
            except AttributeError:
                pass
        
        item_name = child.get('item')
        if item_name:
            items = input.findall(f'.//{item_name}')
            for input_item in items:
                subelement = ET.SubElement(output_element, child[0].tag)
                fill_template(child[0], subelement, input_item)
        else:
            fill_template(child, output_element, input)
