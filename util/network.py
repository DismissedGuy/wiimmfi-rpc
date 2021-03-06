import base64
import logging
import sys
from pathlib import Path

import requests

from .msgboxes import MsgBoxes
from .threading import Thread

data_dir = Path(sys.argv[0]).parent / 'data'
github_headers = {
    'Accept': 'application/vnd.github.v3+json'
}


class GithubDownloadThread(Thread):
    friendly_progress = "Downloading file..."
    permanent = False
    name = 'GithubDownloadThread'

    def __init__(self, method, url, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.method = method
        self.url = url

        self.data = None

    def execute(self):
        file = self.url.split('/')[-1]
        file = file.split('?')[0]  # remove url params

        resp = requests.request(self.method, self.url, headers=github_headers)

        try:
            resp.raise_for_status()
        except requests.RequestException:
            self.log(logging.CRITICAL, 'Failed to restore config files!')

        data = resp.json()
        content = data.get('content')
        message = data.get('message')
        if not content:
            print(MsgBoxes.info(f'Error while restoring config files:\n\n{message}'))
            return
        content = base64.b64decode(content)

        with open(data_dir / file, 'w+') as f:
            f.write(content.decode())

        self.log(logging.INFO, f'Fetched {file}')
