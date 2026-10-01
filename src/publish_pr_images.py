"""Upload rendered PR images and prepare a comment for the trusted workflow."""

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse

from imgur_upload import upload_img

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
MAX_IMAGES = 250
MAX_IMAGE_BYTES = 5 * 1024 * 1024


def find_images(directory):
    images = []
    for path in directory.iterdir():
        if not path.name.endswith('.png'):
            continue
        if not re.fullmatch(r'[1-9][0-9]*\.png', path.name):
            raise ValueError(f'Invalid image filename: {path.name}')
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'Invalid image file: {path.name}')
        if not 8 < path.stat().st_size <= MAX_IMAGE_BYTES:
            raise ValueError(f'Invalid image size: {path.name}')
        with path.open('rb') as f:
            if f.read(8) != PNG_SIGNATURE:
                raise ValueError(f'Invalid PNG signature: {path.name}')
        images.append(path)

    if len(images) > MAX_IMAGES:
        raise ValueError(f'Too many images in artifact: {len(images)}')
    return sorted(images, key=lambda path: int(path.stem))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()

    comments = []
    for path in find_images(args.directory):
        title = f'Template #{path.stem}'
        url, _ = upload_img(str(path), title)
        parsed = urlparse(url)
        if parsed.scheme != 'https' or parsed.hostname != 'i.imgur.com':
            raise ValueError(f'Unexpected Imgur URL for {path.name}')
        comments.append(f'![{title}]({url})')

    body = ''.join(comments) if comments else (
        'No new templates were found, so no images were generated.')
    Path('pr-comment.md').write_text(body)
    print(f'{len(comments)} images uploaded')


if __name__ == '__main__':
    main()
