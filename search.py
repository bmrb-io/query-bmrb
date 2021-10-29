#!/usr/bin/env python3
import os

import pynmrstar

parent_dir = os.path.dirname(os.path.realpath(__file__))


def get_entries():
    for root, subdirs, files in os.walk(os.path.join(parent_dir, 'bmrb_entries')):
        for filename in files:
            yield pynmrstar.Entry.from_file(os.path.join(root, filename))


matching_entries = []
for entry in get_entries():

    # First check if there is a Zinc or Cadmium entity in the entry, and bail if not
    zinc_or_cadmium_entity_ids = []
    entities = entry.get_saveframes_by_category('entity')
    for entity in entities:
        if entity['Nonpolymer_comp_id'][0] == 'ZN' or entity['Nonpolymer_comp_id'][0] == 'CD':
            zinc_or_cadmium_entity_ids.append(entity['ID'])

    if len(zinc_or_cadmium_entity_ids) == 0:
        continue

    # Now check if the specified bonds exist
    # Check out an example NMR-STAR saveframe: https://bmrb.io/data_library/summary/showGeneralSF.php?accNum=30623&Sf_framecode=assembly_1

    # Get the bond loop
    try:
        bond = entry.get_loops_by_category('_Bond')[0]
    except IndexError:
        # No bond information provided
        continue

    # Get the specific tags we care about
    filtered_bond = bond.filter(['Type', 'Comp_ID_1', 'Atom_ID_1', 'Comp_ID_2', 'Entity_ID_2'])

    # Check that we have the right matching values
    matched_entity_ids = set()
    for row in filtered_bond:
        if row[0] == 'coordination' and (row[1] == 'CYS' or row[1] == 'HIS') and row[2] == 'SG' and \
                (row[3] == 'ZN' or row[3] == 'CD'):
            matched_entity_ids.add(row[4])

    # Check that every zinc or cadmium atom is bound
    # This could be tweaked to ensure each ZN/CD is bound twice, etc.
    if len(matched_entity_ids) != len(zinc_or_cadmium_entity_ids):
        continue

    print('Found matching protein: ', entry.entry_id)
    matching_pdb_entries = entry.get_tag('_Related_entries.Database_accession_code')
    if matching_pdb_entries:
        print(f'Matching PDB entries: {matching_pdb_entries}')
    else:
        print('No matching PDB entries')
    sample_conditions = entry.get_loops_by_category('_Sample_condition_variable')
    for sample_condition in sample_conditions:
        filtered = sample_condition.filter(['Type', 'Val', 'Val_units', 'Sample_condition_list_ID'])
        for row in filtered:
            if row[0] == 'pH':
                print(f'In sample ID {row[3]} the pH was {row[1]} {row[2]}.')
            if row[0] == 'temperature':
                print(f'In sample ID {row[3]} the temperature was {row[1]} {row[2]}.')
            if row[0] == 'ionic strength':
                print(f'In sample ID {row[3]} the ionic strength was {row[1]} {row[2]}.')
    # To look at the sample (to get buffer, etc.)
    samples = entry.get_loops_by_category('_Sample_component')
    print('Full sample information:')
    for sample in samples:
        print(sample.format(skip_empty_tags=True))
    print('')
