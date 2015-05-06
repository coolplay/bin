#!/usr/bin/env python
import os
import pprint
import requests

# enter your token here
token = ''

def shell(cmd):
    'Return shell output for ``cmd``'
    return os.popen(cmd).read().strip()


def push(data):
    'Push dict ``data`` containing title and body to server'
    assert isinstance(data, dict)
    url = 'https://api.pushbullet.com/v2/pushes'
    headers = {"Authorization": "Bearer {}".format(token)}
    data.setdefault('type', 'note')
    r = requests.post(url, headers=headers, data=data)
    return r


if __name__ == '__main__':
    # single quote is needed for awk
    ip_addr = shell("ip addr | awk '/inet .*global/{print $2, $NF}'")
    date = shell("date '+%Y-%m-%d %H:%M'")
    hostname = shell("hostname")
    data = dict(title=' '.join([hostname, date]),
                body=ip_addr)

    pprint.pprint(push(data).json())
