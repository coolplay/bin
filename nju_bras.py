#!/usr/bin/env python
# encoding: utf-8
"""Toggle log in status of NJU BRAS in terminal"""

import sys
import argparse
import getpass
import requests

url = 'http://p.nju.edu.cn/portal/portal_io.do'
username = getpass.getpass('User: ') or 'DG1422039'
password = getpass.getpass('Password: ')


class BRAS():
    def __init__(self):
        self.url = url
        self.username = username
        self.password = password
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-i', '--login', action='store_true')
        group.add_argument('-o', '--logout', action='store_true')
        parser.add_argument('-c', '--cookie', action='store_true')
        parser.add_argument('-s', '--status', action='store_true')
        parser.add_argument('-v', '--verbose', action='count', default=0)
        args = parser.parse_args()
        self.args = args
        if args.login:
            self.login()
        elif args.logout:
            self.logout()
        if args.status or not sys.argv[1:]:
            self.info()

    def post(self, data, verbose=False):
        """Do common stuff, return response"""
        try:
            r = requests.post(self.url, data=data)
        except requests.RequestException as e:
            raise Exception('\nNetwork failure')
        try:
            reply = r.json()
        except ValueError as e:
            raise Exception('\nURL redirected:\n{}'.format(r.url))
        #try:
        #    reply = r.json()
        #except Exception as e:
        #    print e
        #    print 'Link Error'
        #    raise SystemExit
        code, msg = reply['reply_code'], reply['reply_message']
        print u'{:<20}{}'.format(code, msg)
        if self.args.verbose and not self.args.login:
            # print "\nDude, I've told you all!"
            return
        elif self.args.verbose >= 1:
            userinfo = reply['userinfo']
            for k, v in userinfo.items():
                if self.args.verbose == 1 and k not in ('service_name',
                                                        'payamount'):
                        continue
                print u'{:<20}{}'.format(k, v)

    def login(self):
        self.post(dict(action = 'login',
                       username = self.username,
                       password = self.password))

    def logout(self):
        self.post(dict(action = 'logout'))

    def info(self):
        self.post(dict(action = 'info'))

if  __name__ == '__main__':
    bras = BRAS()
