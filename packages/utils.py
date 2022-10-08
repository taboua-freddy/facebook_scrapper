

import base64
import requests


def image_as_base64(url: str):
    return base64.b64encode(requests.get(url).content)


