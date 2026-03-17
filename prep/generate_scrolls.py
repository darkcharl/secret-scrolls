#!/usr/bin/env python

import os
import re
import textwrap
import uuid
import xml.dom.minidom

import xmltodict


def load_template(src='templates/_scroll.lsx'):
    with open(src) as fd:
        return xmltodict.parse(fd.read())


def prepare_object(t, spell):
    scroll = t['save']['region']['node']['children']['node']
    for scroll_attribute in scroll['attribute']:
        if scroll_attribute['@id'] == 'DisplayName':
            scroll_attribute['@handle'] = str(uuid.uuid4())
        elif scroll_attribute['@id'] == 'Icon':
            scroll_attribute['@value'] = 'Item_LOOT_SCROLL_Base'
        elif scroll_attribute['@id'] == 'MapKey':
            scroll_attribute['@value'] = str(uuid.uuid4())
        elif scroll_attribute['@id'] == 'Stats':
            scroll_attribute['@value'] = f"OBJ_Scroll_{short_spell_name(spell)}"
    for action_block in scroll['children']['node']['children']['node']:
        # action = action_block['attribute']
        for action_attribute in action_block['children']['node']['attribute']:
            if action_attribute['@id'] == 'SkillID':
                action_attribute['@value'] = spell
            elif action_attribute['@id'] == 'SpellId':
                action_attribute['@value'] = spell
    return t


def write_xml(data, dst):
    with open(dst, 'w') as fd:
        dom = xml.dom.minidom.parseString(xmltodict.unparse(data))
        fd.write(dom.toprettyxml())


def short_spell_name(spell):
    return '_'.join(spell.split('_')[1:])


def split_spell_name(spell):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', short_spell_name(spell))


def compile_item(xml, spell):
    uuid = None
    for attribute in xml['save']['region']['node']['children']['node']['attribute']:
        if attribute['@id'] == 'MapKey':
            uuid = attribute['@value']
    if not uuid:
        raise Exception(f"no uuid found for {spell}")
    name = short_spell_name(spell)
    s = textwrap.dedent(f"""\
        new entry "OBJ_Scroll_{name}"
        type "Object"
        using "_MagicScroll"
        data "RootTemplate" "{uuid}"
        data "ObjectCategory" "MagicScroll"
        data "MinAmount" "1"
        data "MaxAmount" "1"
        data "Priority" "1"

    """)
    return s


def load_enabled_spells():
    with open('Spells_enabled.txt', 'r') as fd:
        return [s.strip() for s in fd.readlines()]


if __name__ == "__main__":
    spells = load_enabled_spells()

    with open('SecretScrolls.xml', 'w+') as localization, \
            open('Object_SecretScrolls.txt', 'w+') as objects:

        """ Initialize localization XML """
        localization.write(textwrap.dedent("""\
            <?xml version="1.0" encoding="utf-8"?>
            <contentList>
        """))

        for spell in spells:
            scroll = None

            """ Find existing scroll file (new LOOT_SCROLL_Name_UUID.lsx or legacy SpellType_Name.lsx) """
            name = short_spell_name(spell)
            import glob as _glob
            existing = _glob.glob(f'generated_scrolls/LOOT_SCROLL_{name}_*.lsx')
            if existing:
                scroll_file = existing[0]
                print(f" [.] loading scroll for {spell} from {scroll_file}")
                with open(scroll_file, 'r') as fd:
                    scroll = xmltodict.parse(fd.read())
            elif os.path.isfile(f'generated_scrolls/{spell}.lsx'):
                scroll_file = f'generated_scrolls/{spell}.lsx'
                print(f" [.] loading scroll for {spell} from legacy file {scroll_file}")
                with open(scroll_file, 'r') as fd:
                    scroll = xmltodict.parse(fd.read())
            else:
                print(f" [>] generating scroll for {spell}")
                scroll = prepare_object(load_template(), spell)
                uuid = None
                for attr in scroll['save']['region']['node']['children']['node']['attribute']:
                    if attr['@id'] == 'MapKey':
                        uuid = attr['@value']
                scroll_file = f'generated_scrolls/LOOT_SCROLL_{name}_{uuid}.lsx'
                write_xml(scroll, scroll_file)

            print(f" [>] writing scroll {spell} to objects")
            objects.write(compile_item(scroll, spell))

            print(f" [>] adding entry {spell} to localization")
            for attribute in scroll['save']['region']['node']['children']['node']['attribute']:
                if attribute['@id'] == 'DisplayName':
                    name_uuid = attribute['@handle']
            data = f'\t<content contentuid="{name_uuid}" version="1">Scroll of {split_spell_name(spell)}</content>\n'
            localization.write(data)

        """ Wrap up localization XML """
        localization.write("</contentList>")
