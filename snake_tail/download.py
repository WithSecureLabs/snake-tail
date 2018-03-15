from os import path

from clint.textui import progress
import requests

from snake_tail import SNAKE_URL


def download(sha256_digest, output_dir=None, json=False, verify=True):
    resp = requests.get(SNAKE_URL + "/download/" + sha256_digest, stream=True, verify=verify)
    if resp.ok:
        file_path = resp.headers['Content-Disposition'].split('filename=')[1].split('"')[1]
        if output_dir:
            file_path = path.join(path.abspath(path.expanduser(output_dir)), file_path)
        with open(file_path, "wb") as f:
            file_size = int(resp.headers['content-length'])
            for chunk in progress.bar(resp.iter_content(chunk_size=1024), expected_size=(file_size / 1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()
    else:
        resp_json = resp.json()
        if json:
            print(resp_json)
        else:
            print("Status: {}".format(resp_json['status'].capitalize()))
            print("Message: {}".format(resp_json['message']))
