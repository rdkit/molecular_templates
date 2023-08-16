import filecmp
import os
import shutil
import tempfile

from rdkit import Chem

HEADER_FILE = 'template_smiles.h'
TEMPLATE_FILE = 'templates.smi'

HEADER_TEXT = """//
//  Copyright (C) 2023 Schrödinger, LLC
//
//   @@ All Rights Reserved @@
//  This file is part of the RDKit.
//  The contents are covered by the terms of the BSD license
//  which is included in the file license.txt, found at the root
//  of the RDKit source tree.
//
// THIS FILE IS AUTOMATICALLY GENERATED. It contains templates used
// in 2D coordinate generation. If you want to contribute to these
// templates, please refer to instructions in:
// https://github.com/rdkit/molecular_templates/blob/main/README.md
//

#include <string>
#include <vector>

// clang-format off
const std::vector<std::string> TEMPLATE_SMILES = {
"""


def clean_smiles(template_smiles):
    """
    Translate all atoms into dummy atoms so that templates are not atom-specific.
    """
    template = Chem.MolFromSmiles(template_smiles)
    for atom in template.GetAtoms():
        atom.SetAtomicNum(0)

    # TO_DO: replace bonds with query bonds

    return Chem.MolToCXSmiles(template)


def generate_header(generated_header_path):
    with open(generated_header_path, 'w') as f_out:
        f_out.write(HEADER_TEXT)
        with open(TEMPLATE_FILE, 'r') as f_in:
            for line in f_in:
                if not (cxsmiles := line.strip()):
                    continue

                # TO_DO: Clean smiles to make them atom-type and bond-type agnostic
                # cxsmiles = clean_smiles(cxsmiles)

                f_out.write(f'    "{cxsmiles}",\n')
        f_out.write('};\n// clang-format on\n')
    print(f"Successfully generated {generated_header_path}")


def check_header_changed(header_file_path):
    if header_changed := not filecmp.cmp(header_file_path, HEADER_FILE):
        if gh_output := os.environ.get('GITHUB_OUTPUT', ''):
            with open(gh_output, 'a') as f:
                f.write(f'header_changed={str(header_changed).lower()}')
    print(f'Header file has {"" if header_changed else "not "}changed')
    return header_changed


def main():
    with tempfile.TemporaryDirectory() as tmpdir:
        generated_header_path = os.path.join(tmpdir, HEADER_FILE)
        generate_header(generated_header_path)

        if check_header_changed(generated_header_path):
            shutil.copy(generated_header_path, HEADER_FILE)
            print(f'Updated {HEADER_FILE} with the generated header')


if __name__ == '__main__':
    main()
