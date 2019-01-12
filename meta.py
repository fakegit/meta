import os
import re
import sys
import json
import select
import random
import argparse
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

with open(sys.path[0] + '/core/headers.json') as file:
    database = json.load(file)

def information(headers):
    result = {}
    for header, value in headers.items():
        if header in database.keys():
            result[header] = database[header]['description']
    return result

def security(headers):
    result = {}
    for header in database:
        if database[header]['security'] == 'yes':
            if header not in headers:
                result[header] = database[header]['description']
    return result

def stdinToHeaders(headers):
    sorted_headers = {}
    for header in headers:
        matches = re.findall(r'(.*):\s(.*)', re.sub(r'\r|\n', '', header))
        for match in matches:
            header = match[0]
            value = match[1]
            try:
                if value[-1] == ',':
                    value = value[:-1]
                sorted_headers[header] = value
            except IndexError:
                pass
    return sorted_headers

headers = {}
piped = select.select([sys.stdin,], [sys.stdin,], [sys.stdin,], 4)[0]

if piped:
    headers = stdinToHeaders(sys.stdin.readlines())
elif args.url:
    headers = requester(args.url).headers
else:
    banner()
    print ('%s No data to act upon.' % bad)
    quit()

if headers:
    if piped:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    headerInformation = information(headers)
    missingHeaders = security(headers)
    if args.jsonOutput:
        jsoned = {}
        jsoned['information'] = headerInformation
        jsoned['security'] = missingHeaders
        sys.stdout.write(json.dumps(jsoned, indent=4))
    else:
        banner()
        if headerInformation:
            print ('%s Header information\n' % info)
            print (json.dumps(headerInformation, indent=4))

        if missingHeaders:
            print ('\n%s Security issues\n' % bad)
            print (json.dumps(missingHeaders, indent=4))