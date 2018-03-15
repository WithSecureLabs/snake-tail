import requests

from snake_tail import SNAKE_URL


def upload(file_type, file_path, name=None, description=None, tags=None, extract=False, password=None, json=False, verify=True):  # pylint: disable=too-many-arguments
    if file_type not in ['file', 'memory']:
        if json:
            print('{"status": "error", "message": "unsupported file type must be \'file\' or \'memory\'"}')
        else:
            print("Status: Error")
            print("Message: unsupported file type must be 'file' or 'memory'")
        return

    data = {}
    if name:
        data['name'] = name
    if description:
        data['description'] = description
    if tags:
        data['tags'] = tags
    if extract:
        data['extract'] = str(extract)
    if password:
        data['password'] = password

    with open(file_path, 'rb') as f:
        resp = requests.post(SNAKE_URL + "/upload/" + file_type, files={"file": f}, json=data, verify=verify)
        resp_json = resp.json()
        if not resp.ok:
            if json:
                print(resp_json)
            else:
                print("Status: {}".format(resp_json['status'].capitalize()))
                print("Message: {}".format(resp_json['message']))
        else:
            if json:
                print(resp_json['data']['sample'])
            else:
                data = resp_json["data"]["sample"]
                for k, v in data.items():
                    print("%-20s:\t%s" % (str(k), str(v)))
