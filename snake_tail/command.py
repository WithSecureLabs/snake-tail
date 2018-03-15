import json as j

import requests

from snake_tail import SNAKE_URL


def command(scale, cmd, sha256_digest, args=None, asynchronous=False, get=False, timeout=None, json=False, verify=True):
    url = SNAKE_URL + "/command"
    if get:
        url += "?sha256_digest={}&scale={}&command={}".format(sha256_digest, scale, cmd)
        resp = requests.get(url, verify=verify)
    else:
        data = {
            'scale': scale,
            'command': cmd,
            'sha256_digest': sha256_digest,
        }
        if args:
            data['args'] = j.loads(args)
        if asynchronous:
            data['asynchronous'] = str(asynchronous)
        if timeout:
            data['timeout'] = timeout
        resp = requests.post(url, json=data, verify=verify)

    resp_json = resp.json()

    if not resp.ok:
        if json:
            print(resp_json)
        else:
            print("Status: {}".format(resp_json['status'].capitalize()))
            print("Message: {}".format(resp_json['message']))
    else:
        if json:
            print(resp_json['data']['command'])
        elif resp_json['data']['command']['status'] != "success":
            print("Status: {}".format(resp_json['data']['command']['status'].capitalize()))
        else:
            output = resp_json['data']['command']['output']
            if isinstance(output, list):
                for row in output:
                    print(row)
            elif isinstance(output, dict):
                for k, v in output.items():
                    print("{}: {}".format(k, v))
            else:
                print(output)
