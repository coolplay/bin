#!/usr/bin/env python
# coding: utf-8
# add attachment: Multipart/mixed (text/plain, application/octet-stream)
# XXX add utf-8 support for filename
# XXX rst/markdown formated message (using rst2html)
"""
To display message body automatically:
    * Gmail needs `Content-Disposition: inline` header for `text`
    * QQ mail displays the first met `text` part in multipart message
To be safe, the message body should be the first part with 'Content-Type' set
to `text` and 'Content-Disposition' set to `inline`
"""
import argparse
import getpass
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

SMTPServer = ("smtp.qq.com", 587)

def send_email(from_addr, to_addrs, passwd, msg):
    server = smtplib.SMTP(*SMTPServer)
    server.ehlo()
    # encrypt
    if server.has_extn('STARTTLS'):
        server.starttls()
        server.ehlo() # re-identify
    server.login(from_addr, passwd)
    server.sendmail(from_addr, to_addrs, msg)
    server.quit()


def msgbody():
    lines = []
    while True:
        try:
            line = raw_input()
        except EOFError:
            break
        except KeyboardInterrupt:
            raise SystemExit
        # if not line:
            # break
        lines.append(line)
    text = MIMEText('\n'.join(lines))
    text.add_header('Content-Disposition', 'inline')
    return text


def msgattach(fname):
    attach = MIMEApplication(open(fname).read())
    attach.add_header('Content-Disposition', 'attachment', filename=fname)
    return attach


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', default='weiwei0132@qq.com', help='from_address')
    parser.add_argument('-t', default='weiwei0132@qq.com', help='to_address')
    parser.add_argument('-s', default='Subject', help='subject')
    parser.add_argument('-a', default='', help='attachment')
    args = parser.parse_args()

    msg = MIMEMultipart()
    msg['Subject'] = args.s
    msg['From'] = args.f
    msg['To'] = args.t
    print 'Ctrl-D to finish or Ctrl-C to cancel'
    msg.attach(msgbody())
    if args.a:
        msg.attach(msgattach(args.a))
    print '{0}\n{1}{0}'.format('~'*70, msg.as_string())
    raw_input()

    print 'Sending...'
    passwd = getpass.getpass('Password: ')
    send_email(args.f, args.t, passwd, msg.as_string())
    print 'Done!'


if __name__ == "__main__":
    main()
