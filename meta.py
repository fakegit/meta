#!/usr/bin/env python

import os
import re
import sys
import json
import random
import argparse
from checks import cors
from checks import cookie
from core.requester import requester
from core.colors import red, green, white, info, bad, end

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help='url', dest='url')
parser.add_argument('--json', help='json output', dest='jsonOutput', action='store_true')
args = parser.parse_args()

def banner():
    newText = ''
    text = '''\n\t{ meta v0.1-beta }\n'''
    for char in text:
        if char != ' ':
            newText += (random.choice([green, white]) + char + end)
        else:
            newText += char
    print (newText)

with open(sys.path[0] + '/db/headers.json') as file:
    database = json.load(file)

def information(headers):
    result = {}
    for header, value in headers.items():
        if header in database.keys():
            result[header] = database[header]['description']
    return result

def missing(headers):
    result = {}
    for header in database:
        if database[header]['security'] == 'yes':
            if header not in headers:
                result[header] = database[header]['description']
    return result

def misconfiguration(headers):
    result = {}
    if 'Access-Control-Allow-Origin' in headers:
        result['Access-Control-Allow-Origin'] = cors.check(args.url)
    if 'Set-Cookie' in headers:
        result['Set-Cookie'] = cookie.check(headers['Set-Cookie'])
    elif 'Cookie' in headers:
        result['Cookie'] = cookie.check(headers['Cookie'])
    return result

headers = {}

if args.url:
    headers = requester(args.url).headers
else:
    banner()
    print ('%s No data to act upon.' % bad)
    quit()

if not args.jsonOutput:
    banner()

if headers:
    headerInformation = information(headers)
    missingHeaders = missing(headers)
    misconfiguration = misconfiguration(headers)
    if args.jsonOutput:
        jsoned = {}
        jsoned['information'] = headerInformation
        jsoned['missing'] = missingHeaders
        jsoned['misconfigurations'] = misconfiguration
        sys.stdout.write(json.dumps(jsoned, indent=4))
    else:
        if headerInformation:
            print ('%s Header information\n' % info)
            print (json.dumps(headerInformation, indent=4))

        if missingHeaders:
            print ('\n%s Missing Headers\n' % bad)
            print (json.dumps(missingHeaders, indent=4))

        if missingHeaders:
            print ('\n%s Mis-configurations\n' % bad)
            print (json.dumps(misconfiguration, indent=4))
