from lxml import etree
from datetime import datetime
import xml.etree.ElementTree as ET
import jinja2 as jja2
import logging as log
import subprocess as sp
import os
import sys
import shutil
import zipfile
import re
import platform
import random, string
import struct


def xml_validator(self):
    try:
        xml_schema = etree.XMLSchema(file=self.xsd_path)
        xml_doc = etree.parse(self.xml_path)
        xml_schema.assertValid(xml_doc)
        results = xml_schema.validate(xml_doc)
        if result:
            log.info(self.xml_path + ' is a valid XML document.')
        return results
    
    except etree.XMLSchemaParseError as xspe:
        print('XMLSchemaParserError occured!')
        print(xspe)
    except etree.XMLSyntaxError as xse:
        # XML failed to validate against schema
        print('DocumentInvalid occured!')
        error = xml_schema.error_log.last_error
        if error:
            # All the error properties describing what went wrong
            print('domain_name: ' + error.domain_name)
            print('domain: '+ str(error.domain))
            print('filename: ' + error.filename)
            print('level: ' + str(error.level))
            print('level_name: ' + error.level_name)
            print('line: ' + str(error.line))
            # a unicode string lists the message
            print('message: ' + error.message)
            print('type: ' + str(error.type))
            print('type_name: ' + error.type_name)
