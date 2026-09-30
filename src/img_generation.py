import argparse
import os

import git
from rdkit import Chem
from rdkit.Chem.Draw import MolDraw2DSVG, MolToImage

img_width = 400
img_height = 400
templates_file = 'templates.smi'


def get_new_templates():
    """
    Finds the new templates that have been added since the base_commit
    """

    with open(templates_file) as f:
        line_nums = {line.strip(): i for i, line in enumerate(f, 1)}

    repo = git.Repo('.')
    tpl_file_diff = repo.git.diff('--', templates_file)

    # Make sure we only generate images for things that have been added,
    # not those we moved around or changed by adding a new line at the end
    added = []
    removed = []

    # We want to skip the diff header, as we don't want to hit the line
    # that says '+++ b/templates.smi'
    changes = tpl_file_diff.split('\n')
    for line in changes[4:]:
        if line.startswith('-') and (cxsmiles := line[1:].strip()):
            removed.append(cxsmiles)
        elif line.startswith('+') and (cxsmiles := line[1:].strip()):
            added.append(cxsmiles)

    for cxsmiles in added:
        if cxsmiles not in removed:
            yield line_nums[cxsmiles], cxsmiles


def draw_png(cxsmiles, idx, output_dir='.'):
    smiles = cxsmiles.split()[0]
    legend = f"#{idx} {smiles}"
    mol = Chem.MolFromSmiles(cxsmiles)
    if not mol.GetNumConformers():
        raise ValueError("SMILES must include coordinates")

    print(f'Creating PNG image #{idx} for SMILES "{smiles}"')

    fpath = os.path.join(output_dir, f'{idx}.png')
    png = MolToImage(mol, size=(img_width, img_height), legend=legend)
    png.save(fpath)
    return fpath, legend


def draw_svg(cxsmiles, fname, legend):
    mol = Chem.MolFromSmiles(cxsmiles)
    if not mol.GetNumConformers():
        raise ValueError("SMILES must include coordinates")

    print(f'Creating SVG image {legend}: {fname}')

    drawer = MolDraw2DSVG(img_width, img_height)
    drawer.DrawMolecule(mol, legend=legend)
    drawer.FinishDrawing()

    with open(fname, 'w') as f:
        f.write(drawer.GetDrawingText())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    count = 0
    for idx, cxsmiles in get_new_templates():
        draw_png(cxsmiles, idx, args.output_dir)
        count += 1

    print(f'{count} images generated')


if __name__ == '__main__':
    main()
