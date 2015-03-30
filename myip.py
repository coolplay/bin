#!/usr/bin/env python
# get IP address of local host
import socket
socket.setdefaulttimeout(1)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(("www.baidu.com", 80))
except socket.error:
    pass
finally:
    print 'local\t{}'.format(s.getsockname()[0])
    # print 'remote\t{}'.format(s.getpeername()[0])
    s.close()

