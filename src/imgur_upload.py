import json
import os
from base64 import b64encode

from requests_oauthlib import OAuth2Session, TokenUpdated

ALBUM_HASH = ''
IMGUR_UPLOAD_URL = "https://api.imgur.com/3/upload.json"
UPLOAD_RETRIES = 5

IMGUR_CLIENT_ID = os.environ.get('IMGUR_CLIENT_ID', None)
IMGUR_TOKEN = json.loads(os.environ.get('IMGUR_TOKEN', '[]'))


def upload_img(fpath, title):

    img = b64encode(open(fpath, 'rb').read())
    fname = os.path.basename(fpath)

    data = {'image': img, 'type': 'base64', 'name': fname, 'title': title}
    if ALBUM_HASH:
        data['album'] = ALBUM_HASH

    session = OAuth2Session(client_id=IMGUR_CLIENT_ID, token=IMGUR_TOKEN)

    for _ in range(UPLOAD_RETRIES):
        try:
            request = session.post(IMGUR_UPLOAD_URL, data=data)
        except TokenUpdated:
            # The token should expire in ~10 years. Automatic renewal requires
            # setting up some more complex infra and permissions I'm not happy
            # to grant, so we'll deal with this manually when it happens.
            raise RuntimeError('imgur access token expired')
        if request.ok:
            break
    if not request.ok:
        raise RuntimeError(request.text)

    return request.json()['data']['link'], title
