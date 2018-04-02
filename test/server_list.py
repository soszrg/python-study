#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pprint
import sys

# print sys.argv

server_dict = {
    "182.61.10.117": ["device_a"],
    "182.61.53.227": ["device_b", "migration"],
    "182.61.36.65": ["api_web_a", "consumer_1"],
    "182.61.59.169": ["api_web_b", "consumer_2"],
    "182.61.55.225": ["dev"],
}

pprint.pprint(server_dict)

if len(sys.argv) != 2:
    print "server name error"
    exit(-1)

server_name = sys.argv[1]

ip = None
for server_ip, server_name_list in server_dict.items():
    if server_name in server_name_list:
        ip = server_ip
        break

if not ip:
    print "="*30
    print "Server name error"
    print "="*30
    exit(-1)

print "\n\nroot@%s" % ip

