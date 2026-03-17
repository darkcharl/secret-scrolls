#!/usr/bin/env python
"""
Rename template files from SpellType_SpellName.{lsx,lsf} to
LOOT_SCROLL_SpellName_UUID.{lsx,lsf} to match BG3 vanilla naming conventions.

Also patches the Name attribute in LSX files when it is empty (so LSF
recompilation produces templates with the correct Name value).

Run from the prep/ directory.
"""

import os
import re
import xml.etree.ElementTree as ET


def get_lsx_attrs(path):
    tree = ET.parse(path)
    root = tree.getroot()
    name = ''
    mapkey = ''
    stats = ''
    for attr in root.iter('attribute'):
        aid = attr.get('id')
        if aid == 'Name':
            name = attr.get('value', '')
        elif aid == 'MapKey':
            mapkey = attr.get('value', '')
        elif aid == 'Stats':
            stats = attr.get('value', '')
    return name, mapkey, stats


def patch_lsx_name(path, loot_name):
    """Set the Name attribute in the LSX file to loot_name if it is currently empty."""
    tree = ET.parse(path)
    root = tree.getroot()
    patched = False
    for attr in root.iter('attribute'):
        if attr.get('id') == 'Name' and attr.get('value', '') == '':
            attr.set('value', loot_name)
            patched = True
            break
    if patched:
        ET.indent(tree, space='\t')
        tree.write(path, encoding='unicode', xml_declaration=True)
        print(f'  [p] patched Name="{loot_name}" in {os.path.basename(path)}')


def rename_pair(directory, old_stem, new_stem):
    for ext in ('.lsx', '.lsf'):
        old = os.path.join(directory, old_stem + ext)
        new = os.path.join(directory, new_stem + ext)
        if os.path.exists(old):
            if old == new:
                print(f'  [=] already correct: {old_stem}{ext}')
            else:
                os.rename(old, new)
                print(f'  [>] {old_stem}{ext}  ->  {new_stem}{ext}')
        else:
            print(f'  [-] missing: {old_stem}{ext}')


def process_dir(directory, name_source):
    """
    name_source: 'Name' to use LSX Name attr (PAK files with Name already set),
                 'Stats' to derive from Stats attr and patch LSX Name attr
    """
    lsx_files = sorted(f for f in os.listdir(directory) if f.endswith('.lsx'))
    for fname in lsx_files:
        path = os.path.join(directory, fname)
        name, mapkey, stats = get_lsx_attrs(path)

        if name_source == 'Name':
            loot_name = name
        else:
            # Stats = "OBJ_Scroll_AnimalFriendship" -> "LOOT_SCROLL_AnimalFriendship"
            loot_name = 'LOOT_SCROLL_' + re.sub(r'^OBJ_Scroll_', '', stats)
            patch_lsx_name(path, loot_name)

        if not loot_name or not mapkey:
            print(f'  [!] skipping {fname} — could not determine name or uuid')
            continue

        old_stem = fname[:-4]  # strip .lsx
        new_stem = f'{loot_name}_{mapkey}'
        rename_pair(directory, old_stem, new_stem)


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scrolls_root = os.path.join(script_dir, '../..')

    dirs = [
        (os.path.join(script_dir, '../PAK/Public/SecretScrolls/RootTemplates'), 'Name'),
        (os.path.join(script_dir, 'generated_scrolls'), 'Stats'),
        (os.path.join(scrolls_root, 'SecretScrollsExtended/PAK/Public/SecretScrollsExtended/RootTemplates'), 'Stats'),
        (os.path.join(scrolls_root, 'SecretScrollsUnlocked/PAK/Public/SecretScrollsUnlocked/RootTemplates'), 'Stats'),
    ]

    for directory, name_source in dirs:
        directory = os.path.normpath(directory)
        print(f'\n=== {directory} ===')
        if os.path.isdir(directory):
            process_dir(directory, name_source)
        else:
            print('  [!] directory not found')
