"""
Functions performing XML conversion from one format to another
based on a template defined by nested TransElements.
"""
from typing import Type
import xml.etree.ElementTree as ET

class TransElement(ET.Element):
    def __init__(self, tag, from_id=None, repeated_child=None, transform=lambda x: x, children=[]):
        self.from_id = from_id
        self.repeated_child = repeated_child
        self.transform = transform
        super().__init__(tag)
        for child in children:
            super().append(child)
    
    def replicate(self):
        replicated_children = []
        for child in self:
            replicated_children.append(child.replicate())
        replica = TransElement(self.tag, self.from_id, self.repeated_child, self.transform, children=replicated_children)

        return replica

    def fill_from_source(self, sourcetree_element):

        if self.from_id is not None:
            # find and fill the value applying the tranformation function
            source_element = sourcetree_element.find(f'.//datapoint/[@schema_id="{self.from_id}"]')
            try:
                source_value = source_element.text
                self.text = self.transform(source_value)
            except Exception as e:
                print(repr(e))

        if self.repeated_child is not None:
            # get the source elements
            source_elements = sourcetree_element.findall(f'.//tuple/[@schema_id="{self.repeated_child}"]')
        
            # call fill on each child with appropriate element
            for i in range(len(source_elements) - 1):
                # create n-1 duplicates of the (only) child
                copied_element = self[0].replicate()
                self.append(copied_element)
            
            for child_template, source_el in zip(self, source_elements):
                # fill each child with values from corresponding source element
                child_template.fill_from_source(source_el)

        else: # no repeated children
            for child in self:
                child.fill_from_source(sourcetree_element)

def convert_xml(input_xml):
    """
    Return XML converted from input_xml to a fromat specified by the template.
    """
    template = TransElement('InvoiceRegisters', children=[
        TransElement('Invoices', children=[
            TransElement('Payable', children=[
                TransElement('InvoiceNumber', from_id='document_id'),
                TransElement('InvoiceDate', from_id='date_issue', transform=lambda date: date + "T00:00:00"),
                TransElement('DueDate', from_id='date_due', transform=lambda date: date + "T00:00:00"),
                TransElement('TotalAmount'),
                TransElement('Notes'),
                TransElement('Iban', from_id='iban'),
                TransElement('Amount', from_id='amount_total_tax'),
                TransElement('Currency', from_id='currency', transform=lambda symbol: symbol.upper()),
                TransElement('Vendor', from_id='sender_name'),
                TransElement('VendorAddress', from_id='sender_address'),
                TransElement('Details', repeated_child='line_item', children=[
                    TransElement('Detail', children=[
                        TransElement('Amount', from_id='item_total_base'),
                        TransElement('AccountId'),
                        TransElement('Quantity', from_id='item_quantity'),
                        TransElement('Notes', from_id='item_description', transform=lambda note: note.replace('\n', ' '))
                    ])
                ])
            ])
        ])
    ])

    input_root = ET.fromstring(input_xml)

    template.fill_from_source(input_root)
    ET.indent(template)

    with open('input.xml', 'wb') as f:
        ET.indent(input_root)
        input_tree = ET.ElementTree(element=input_root)
        input_tree.write(f)

    with open('converted.xml', 'wb') as f:
        temp_tree = ET.ElementTree(element=template)
        temp_tree.write(f)
    
    return ET.tostring(template)