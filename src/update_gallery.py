import glob
import hashlib
import os

from img_generation import draw_svg

gallery_file = 'gallery.md'
img_dir = "img"
img_width = 400
img_height = 400
tpl_file = 'templates.smi'


def get_hash(s):
    data = s.encode('utf-8').strip()
    return hashlib.sha256(data).hexdigest()


def get_new_templates():
    with open(tpl_file, 'r') as f:
        for i, line in enumerate(f, 1):
            yield i, line.strip()


def generate_gallery(templates):
    with open(gallery_file, 'w') as f:
        f.write('# Templates\n\n')
        for smiles, img in templates:
            f.write(f'![{smiles}]({img})')


def clean_up_imgs(templates):
    existing_imgs = set(glob.glob(os.path.join(img_dir, '*.svg')))
    current_imgs = [img for _, img in templates]
    for fname in existing_imgs.difference(current_imgs):
        print(f'Removing outdated SVG {fname}')
        os.remove(fname)


def main():
    os.makedirs(img_dir, exist_ok=True)

    templates = []
    for idx, cxsmiles in get_new_templates():
        fname = os.path.join(img_dir, f'{get_hash(cxsmiles)}.svg')
        smiles = cxsmiles.split()[0]
        if not os.path.isfile(fname):
            draw_svg(cxsmiles, fname, f"#{idx} {smiles}")
        templates.append((smiles, fname))

    generate_gallery(templates)
    clean_up_imgs(templates)


if __name__ == '__main__':
    main()
