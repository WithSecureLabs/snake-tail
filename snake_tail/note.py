import requests

from snake_tail import SNAKE_URL


def note(sha256_digest, create=False, delete=False, update=False, body=None, json=False, verify=True):
    url = SNAKE_URL + "/note/" + sha256_digest
    if create:
        data = {'sha256_digest': sha256_digest}
        if body:
            data['body'] = body
        resp = requests.post(SNAKE_URL + "/note", json=data, verify=verify)
    elif delete:
        resp = requests.delete(url, verify=verify)
    elif update:
        data = {}
        if body:
            data['body'] = body
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
                print("Note successfully deleted")
                return
            print(resp_json["data"]["note"]["body"])
