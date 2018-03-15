import json as j

import requests

from snake_tail import SNAKE_URL


def info(scale, reload=False, json=False, verify=True):
    resp = requests.get(SNAKE_URL + "/scale/" + scale + '?reload=' + str(reload), verify=verify)
    resp_json = resp.json()
    if not resp.ok:
        if json:
            print(resp_json)
        else:
            print("Status: {}".format(resp_json['status'].capitalize()))
            print("Message: {}".format(resp_json['message']))
    else:
        scale_info = resp_json["data"]["scale"]
        if json:
            components = {}
            if 'commands' in scale_info['components']:
                resp = requests.get(SNAKE_URL + "/scale/" + scale + "/commands", verify=verify)
                components['commands'] = resp.json()['data']['commands']
            if 'interface' in scale_info['components']:
                resp = requests.get(SNAKE_URL + "/scale/" + scale + "/interface", verify=verify)
                components['interface'] = resp.json()['data']['interface']
            if 'upload' in scale_info['components']:
                resp = requests.get(SNAKE_URL + "/scale/" + scale + "/upload", verify=verify)
                components['upload'] = resp.json()['data']['upload']
            scale_info['components'] = components
            print(scale_info)
        else:
            print("%-15s:\t%s" % ("Name", scale_info["name"]))
            print("%-15s:\t%s" % ("Description", scale_info["description"]))
            print("%-15s:\t%s" % ("Version", scale_info["version"]))
            print("%-15s:\t%s" % ("Author", scale_info["author"]))
            print("%-15s:\t%s" % ("Supports", ', '.join([str(item) for item in scale_info["supports"]])))

            # Fetch the components
            if 'commands' in scale_info['components']:
                print("\nCommands:")
                resp = requests.get(SNAKE_URL + "/scale/" + scale + "/commands", verify=verify)
                for each_command in resp.json()["data"]["commands"]:
                    print("\t%-15s:\t%-15s" % ("Command", each_command["command"]))
                    print("\t%-15s:\t%-15s" % ("Info", each_command["info"]))
                    print("\t%-15s:\t%-15s" % ("Arguments", each_command["args"]))
                    print("")
            if 'interface' in scale_info['components']:
                print("\nInterface:")
                resp = requests.get(SNAKE_URL + "/scale/" + scale + "/interface", verify=verify)
                for each_command in resp.json()["data"]["interface"]["pullers"]:
                    print("\t%-15s:\t%-15s" % ("Command", each_command["command"]))
                    print("\t%-15s:\t%-15s" % ("Info", each_command["info"]))
                    print("\t%-15s:\t%-15s" % ("Arguments", each_command["args"]))
                    print("\t%-15s:\t%-15s" % ("Type", "Pull"))
                    print("")
                for each_command in resp.json()["data"]["interface"]["pushers"]:
                    print("\t%-15s:\t%-15s" % ("Command", each_command["command"]))
                    print("\t%-15s:\t%-15s" % ("Info", each_command["info"]))
                    print("\t%-15s:\t%-15s" % ("Arguments", each_command["args"]))
                    print("\t%-15s:\t%-15s" % ("Type", "Push"))
                    print("")
            if 'upload' in scale_info['components']:
                print("\nUpload:")
                resp = requests.get(SNAKE_URL + "/scale/" + scale + "/upload", verify=verify)
                upld = resp.json()["data"]["upload"]
                print("\t%-15s:\t%-15s" % ("Info", upld["info"]))
                print("\t%-15s:\t%-15s" % ("Arguments", upld["args"]))
                print("")


def interface(scale, command, sha256_digest, args=None, type=None, json=False, verify=True):  # pylint: disable=redefined-builtin
    url = SNAKE_URL + "/scale/" + scale + '/interface'
    data = {
        'command': command,
        'sha256_digest': sha256_digest,
    }
    if args:
        data['args'] = j.loads(args)
    if type:
        data['type'] = str(type)
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
            print(resp_json['data']['interface'])
        else:
            output = resp_json['data']['interface']
            if isinstance(output, list):
                for row in output:
                    print(row)
            elif isinstance(output, dict):
                for k, v in output.items():
                    print("{}: {}".format(k, v))
            else:
                print(output)


def scales(reload=False, json=False, verify=True):
    resp = requests.get(SNAKE_URL + "/scales?reload=" + str(reload), verify=verify)
    resp_json = resp.json()
    if not resp.ok:
        if json:
            print(resp_json)
        else:
            print("Status: {}".format(resp_json['status'].capitalize()))
            print("Message: {}".format(resp_json['message']))
    else:
        if json:
            print(resp_json['data']['scales'])
        else:
            data = sorted(resp_json["data"]["scales"], key=lambda k: k['name'])
            for i in data:
                print(i["name"])


def upload(scale, args, name=None, description=None, tags=None, extract=False, password=None, json=False, verify=True):  # pylint: disable=too-many-arguments
    data = {"args": j.loads(args)}
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
    resp = requests.post(SNAKE_URL + "/scale/" + scale + '/upload', json=data, verify=verify)
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
