import json as j

import requests

from snake_tail import SNAKE_URL


def samples(file_type=None, limit=None, filter=None, operator=None, order=None, sort=None, json=False, verify=True, from_=None):  # pylint: disable=redefined-builtin
    url = SNAKE_URL + "/store"
    args = []
    if file_type:
        args += ['file_type={}'.format(file_type)]
    if from_:
        args += ['from={}'.format(from_)]
    if limit:
        args += ['limit={}'.format(limit)]
    if filter:
        for k, v in j.loads(filter).items():
            args += ['filter[%s]={"$regex":"%s", "$options": "-i"}' % (k, v)]
    if operator:
        args += ['operator={}'.format(operator)]
    if order:
        args += ['order={}'.format(order)]
    if sort:
        args += ['sort={}'.format(sort)]

    if args:
        url += "?" + '&'.join(args)

    resp = requests.get(url, verify=verify)
    resp_json = resp.json()
    if not resp.ok:
        if json:
            print(resp_json)
        else:
            print("Status: {}".format(resp_json['status'].capitalize()))
            print("Message: {}".format(resp_json['message']))
    else:
        data = resp_json["data"]["samples"]
        if json:
            print(data)
        else:
            for i in data:
                print("%s\t%s\t%s\t%-25s\t%s" % (i["sha256_digest"], i["timestamp"], i["file_type"], i["mime"], i["name"]))
