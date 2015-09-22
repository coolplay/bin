#!/usr/bin/env python2
import argparse
import getpass
import hashlib
import requests

username = 'dg1422039'
password = '' # your password
base_url = 'http://p.nju.edu.cn'
io_url = base_url + '/portal_io/'


def get_challenge():
    'Get challenge string'
    url = io_url + 'getchallenge'
    r = requests.post(url)
    return r.json()['challenge']


def hex2chr(str):
    'Return chr string from hex string'
    return ''.join(chr(int(str[i:i+2], base=16))
            for i in range(0, len(str), 2))


def md5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


def create_chap_password(challenge, password):
    'Get CHAP password string'
    id = 102 # >= 16
    raw = chr(id) + password + hex2chr(challenge)
    chap_password = hex(id).lstrip('0x') + md5(raw)
    return chap_password


def login(password):
    url = io_url + 'login'
    challenge = get_challenge()
    chap_password = create_chap_password(challenge, password)
    params = {
            'username': username,
            'password': chap_password,
            'challenge': challenge
            }
    r = requests.post(url, params)
    return r.json()


def logout():
    url = io_url + 'logout'
    r = requests.post(url)
    return r.json()

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Login NJU BRAS')
    parser.add_argument('--logout', '-o', action='store_true', help='Log out')
    parser.add_argument('--verbose', '-v', action='store_true', help='Print more information')
    args = parser.parse_args()
    json = logout() if args.logout else login(password or getpass.getpass())
    if args.verbose:
        f = u'{:>20}  {}'
        for k, v in json.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    print f.format(kk, vv)
            else:
                print f.format(k, v)
    else:
        print json['reply_msg']
