import requests

from snake_tail import SNAKE_URL


def file(sha256_digest, delete=False, update=False, name=None, description=None, tags=None, json=False, verify=True):
    url = SNAKE_URL + "/file/" + sha256_digest
    if delete:
        resp = requests.delete(url, verify=verify)
    elif update:
        data = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if tags:
            data['tags'] = tags
        resp = requests.patch(url, json=data, verify=verify)
    else:
        resp = requests.get(url, verify=verify)

    resp_json = resp.json()

    if not resp.ok:
        if json:
            print(resp_json)
        else:
            print("Status: {}".format(resp_json['status'].capitalize()))
            print("Message: {}".format(resp_json['message']))
    else:
        if json:
            print(resp_json['data'])
        else:
            if delete:
                print("File successfully deleted")
                return
            data = resp_json["data"]["file"]
            for k, v in data.items():
                print("%-20s:\t%s" % (str(k), str(v)))
