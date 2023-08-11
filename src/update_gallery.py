import glob
import hashlib
import os

from rdkit import Chem
from rdkit.Chem.Draw import MolDraw2DSVG

GALLERY_FILE = os.environ.get('GALLERY_FILE', 'gallery.md')
IMG_DIR = os.environ.get('IMG_DIR', 'img')
TPL_FILE = os.environ.get('TPL_FILE', 'templates.smi')
BASE_SHA = os.environ.get('GH_PR_BASE', 'main')
REPO_URL = os.environ.get('GH_REPO_URL', 'main')

IMG_SIZE = (400, 400)


def get_hash(s):
    data = s.encode('utf-8').strip()
    return hashlib.sha256(data).hexdigest()


def get_all_templates():
    with open(TPL_FILE, 'r') as f:
        for i, line in enumerate(f, 1):
            yield i, line.strip()


def get_img_markdown(legend, fname):
    """
    Return 2 markdown strings for the image:
    - one for the PR comment, with a full url to the fork that originated the PR
    - one for the gallery, with a relative url to the main repo
    """
    return f'![{legend}]({fname})', f'![{legend}]({REPO_URL}/{fname})'


def draw_svg(cxsmiles, fname, legend):
    mol = Chem.MolFromSmiles(cxsmiles)
    if not mol.GetNumConformers():
        raise ValueError("SMILES must include coordinates")

    print(f'Creating SVG image {legend}: {fname}')

    drawer = MolDraw2DSVG(*IMG_SIZE)
    drawer.DrawMolecule(mol, legend=legend)
    drawer.FinishDrawing()

    with open(fname, 'w') as f:
        f.write(drawer.GetDrawingText())


def generate_gallery(templates):
    with open(GALLERY_FILE, 'w') as f:
        f.write('# Templates\n\n')
        for smiles, _, md in templates:
            f.write(f'![{smiles}]({md})')


def clean_up_imgs(templates):
    existing_imgs = set(glob.glob(os.path.join(IMG_DIR, '*.svg')))
    current_imgs = [img for _, img, _ in templates]
    for fname in existing_imgs.difference(current_imgs):
        print(f'Removing outdated SVG {fname}')
        os.remove(fname)


def export_pr_image_urls(pr_imgs):
    if gh_output := os.environ.get('GITHUB_OUTPUT', ''):
        with open(gh_output, 'a') as f:
            f.write(f"pr_images=\"{''.join(pr_imgs)}\"")


def main():
    os.makedirs(IMG_DIR, exist_ok=True)

    pr_imgs = []
    all_templates = []
    for idx, cxsmiles in get_all_templates():
        hash = get_hash(f'{idx} {cxsmiles}')
        fname = os.path.join(IMG_DIR, f'{hash}.svg')
        smiles = cxsmiles.split()[0]
        title = f"#{idx} {smiles}"
        img_main_md, img_pr_md = get_img_markdown(title, fname)
        if not os.path.isfile(fname):
            pr_imgs.append(img_pr_md)
            draw_svg(cxsmiles, fname, title)
        all_templates.append((smiles, fname, img_main_md))

    generate_gallery(all_templates)
    clean_up_imgs(all_templates)
    export_pr_image_urls(pr_imgs)


if __name__ == '__main__':
    main()
