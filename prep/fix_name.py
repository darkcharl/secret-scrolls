#!/usr/bin/env python

import glob
import xml.dom.minidom

import xmltodict
import pprint


class IconNotFoundException(Exception):
    def __init__(self, msg="icon not found"):
        self.message = msg


def fix_name_using_icon(xml):
    
    scroll_game_object = xml['save']['region']['node']['children']['node']
    icon = ""
    for attribute in scroll_game_object['attribute']:
        if attribute['@id'] == 'Icon':
            icon = attribute['@value']
    if not icon:
        raise IconNotFoundException
    
    for attribute in scroll_game_object['attribute']:
        if attribute['@id'] == 'Name':
            attribute['@value'] = '_'.join(icon.split('_')[1:])

    return xml


def fix_name(scroll_file):
    with open(scroll_file, "r") as fd:
        x = xmltodict.parse(fd.read())

    x = fix_name_using_icon(x)

    with open(f'{scroll_file}', 'w+') as fd:
        dom = xml.dom.minidom.parseString(xmltodict.unparse(x))
        fd.write(dom.toprettyxml())


if __name__ == "__main__":
    rt_path = "../PAK/Public/SecretScrolls/RootTemplates/*.lsx"
    for scroll_file in glob.glob(rt_path, recursive=True):
        print(f" [*] {scroll_file}")
        fix_name(scroll_file)
