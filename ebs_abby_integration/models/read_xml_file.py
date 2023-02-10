import xml.etree.ElementTree as ET
import os

def read_xmlFile():

    tree = ET.parse('temp_image.xml')
    root = tree.getroot()
    address = ""
    phone=""
    email=""
    web=""
    name=""
    company=""
    job=""
    for child in root:
        if child.tag =="{http://ocrsdk.com/schema/recognizedBusinessCard-1.0.xsd}businessCard":
            for attr in child:
                if attr.tag == '{http://ocrsdk.com/schema/recognizedBusinessCard-1.0.xsd}field':
                    for nodes in attr:
                        if attr.get('type') == "Phone":
                            phone = nodes.text
                        elif attr.get('type') == "Email":
                            email = nodes.text
                        elif attr.get('type') == "Web":
                            web = nodes.text
                        elif attr.get('type') == "Name":
                            name = nodes.text
                        elif attr.get('type') == "Company":
                            company = nodes.text
                        elif attr.get('type') == "Job":
                            job = nodes.text
                        elif attr.get('type') == "Address":
                            address = nodes.text
    return phone,email,web,name,company,job,address








