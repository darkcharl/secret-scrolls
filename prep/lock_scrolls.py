#!/usr/bin/env python

import glob
import xml.dom.minidom

import xmltodict


class SpellNotFoundException(Exception):
    def __init__(self, msg="spell not found"):
        self.message = msg


def add_class_lock(xml, class_id="a865965f-501b-46e9-aa9e-4877c0e8094d"):
    scroll = xml['save']['region']['node']['children']['node']
    for action_block in scroll['children']['node']['children']['node']:
        action = action_block['attribute']
        if action['@value'] == '12':
            spell_name = ""
            conditional = False
            action_attributes = action_block['children']['node']['attribute']
            for action_attribute in action_attributes:
                if action_attribute['@id'] == 'SkillID':
                    spell_name = action_attribute['@value']
                elif action_attribute['@id'] == "Conditions":
                    conditional = True
                    break

            if not spell_name:
                raise SpellNotFoundException

            if conditional:
                continue

            condition = {
                '@id': 'Conditions',
                '@type': 'LSString',
                '@value': f'CanUseSpellScroll("{spell_name}")',
            }
            action_attributes.append(condition)
            class_id = {
                '@id': 'ClassId',
                '@type': 'guid',
                '@value': class_id,
            }
            action_attributes.append(class_id)
    return xml


def lock_scroll(scroll_file):
    with open(scroll_file, "r") as fd:
        x = xmltodict.parse(fd.read())

    x = add_class_lock(x)

    with open(f'{scroll_file}', 'w+') as fd:
        dom = xml.dom.minidom.parseString(xmltodict.unparse(x))
        fd.write(dom.toprettyxml())


if __name__ == "__main__":
    rt_path = "../PAK/Public/SecretScrolls/RootTemplates/*.lsx"
    for scroll_file in glob.glob(rt_path, recursive=True):
        print(f" [*] {scroll_file}")
        lock_scroll(scroll_file)
