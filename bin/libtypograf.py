"""
A better library to use https://www.artlebedev.ru/tools/typograf/
"""

import xml.etree.cElementTree as ET
from io import BytesIO
from urllib.request import Request, urlopen
import re


__all__ = ['typograf']


def typograf(text):
    request = envelope(text)
    response = send_request(request)
    result = parse_response(response)
    return result


def envelope(text, entityType=3, useBr=1, useP=0, maxNobr=3):
    ET.register_namespace('soap', 'http://schemas.xmlsoap.org/soap/envelope/')
    ET.register_namespace('', 'http://typograf.artlebedev.ru/webservices/')

    envelopeElem = ET.Element('{http://schemas.xmlsoap.org/soap/envelope/}Envelope')
    bodyElem = ET.SubElement(envelopeElem, '{http://schemas.xmlsoap.org/soap/envelope/}Body')
    processTextElem = ET.SubElement(bodyElem, '{http://typograf.artlebedev.ru/webservices/}ProcessText')
    textElem = ET.SubElement(processTextElem, '{http://typograf.artlebedev.ru/webservices/}text')
    textElem.text = text
    entityTypeElem = ET.SubElement(processTextElem, '{http://typograf.artlebedev.ru/webservices/}entityType')
    entityTypeElem.text = str(entityType)
    useBrElem = ET.SubElement(processTextElem, '{http://typograf.artlebedev.ru/webservices/}useBr')
    useBrElem.text = str(useBr)
    usePElem = ET.SubElement(processTextElem, '{http://typograf.artlebedev.ru/webservices/}useP')
    usePElem.text = str(useP)
    maxNobrElem = ET.SubElement(processTextElem, '{http://typograf.artlebedev.ru/webservices/}maxNobr')
    maxNobrElem.text = str(maxNobr)

    tree = ET.ElementTree(envelopeElem)
    xml = BytesIO()
    tree.write(xml, encoding='utf-8', xml_declaration=True)
    return xml.getvalue()


def send_request(xmlbody):
    request = Request(
        url='http://typograf.artlebedev.ru/webservices/typograf.asmx',
        data=xmlbody,
        headers={
            'SOAPAction': '"http://typograf.artlebedev.ru/webservices/ProcessText"',
            'Content-Type': 'text/xml'
        },
        method='POST'
    )
    response = urlopen(request).read().decode('utf-8')
    return response


def parse_response(response):
    response = re.sub(r'^<\?xml.+\?>', '', response)     # xml declaration doesn't contain encoding, removing it
    xml = ET.fromstring(response)
    text = xml.findtext('.//{http://typograf.artlebedev.ru/webservices/}ProcessTextResult')
    text = text.replace('<br />\n', '\n')
    text = text.replace('<br />', '\n')
    return text
