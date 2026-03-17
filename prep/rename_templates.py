#!/usr/bin/env python
"""
Rename template files from SpellType_SpellName.{lsx,lsf} to
LOOT_SCROLL_SpellName_UUID.{lsx,lsf} to match BG3 vanilla naming conventions.

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
    name_source: 'Name' to use LSX Name attr (PAK files),
                 'Stats' to derive from Stats attr (prep files, where Name=="")
    """
    lsx_files = sorted(f for f in os.listdir(directory) if f.endswith('.lsx'))
    for fname in lsx_files:
        path = os.path.join(directory, fname)
        name, mapkey, stats = get_lsx_attrs(path)

        if name_source == 'Name':
            loot_name = name
        else:
            # Stats = "OBJ_Scroll_AnimalFriendship" → "LOOT_SCROLL_AnimalFriendship"
            loot_name = 'LOOT_SCROLL_' + re.sub(r'^OBJ_Scroll_', '', stats)

        if not loot_name or not mapkey:
            print(f'  [!] skipping {fname} — could not determine name or uuid')
            continue

        old_stem = fname[:-4]  # strip .lsx
        new_stem = f'{loot_name}_{mapkey}'
        rename_pair(directory, old_stem, new_stem)


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))

    pak_dir = os.path.join(script_dir, '../PAK/Public/SecretScrolls/RootTemplates')
    prep_dir = os.path.join(script_dir, 'generated_scrolls')

    print('\n=== PAK/Public/SecretScrolls/RootTemplates ===')
    process_dir(pak_dir, name_source='Name')

    print('\n=== prep/generated_scrolls ===')
    process_dir(prep_dir, name_source='Stats')
