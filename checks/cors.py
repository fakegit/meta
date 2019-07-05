import re
import requests
import db.tlds
from urllib.parse import urlparse

def check(url):
    url = re.sub('^https?://', '', url)                # url w/o proto
    host = urlparse('//'+url).hostname or ''  # set hostname
    acao = make_request(url, url, False, True)                 # perform request
    if acao:
        if (acao == 'no_acac' or '*' == acao):
            return
        if acao == '*':
            return '* (without credentials)'
        elif acao in ['//', '://']:
            return 'Any origin allowed' # firefox/chrome/safari/opera only
        elif re.findall(r'\s|,|\|', acao):
            return 'Multiple values in Access-Control-Allow-Origin'
        elif re.findall(r'\*.', acao):
            return 'Wrong use of wildcard, only single '*' is valid'
        elif re.findall(r'fiddle.jshell.net|s.codepen.io', acao):
            return 'Developer backdoor'
        elif 'sub.'+host in make_request(url, 'sub.'+url):
            return 'Arbitrary subdomains allowed'
        elif make_request(url, url, True).startswith('http://'):
            return 'Non-ssl site allowed'
        elif 'evil.org' in make_request(url, 'evil.org'):
            return 'Origin reflection'
        elif 'not'+host in make_request(url, 'not'+url):
            if sld(host):
                return 'Pre-domain wildcard'
            else:
                return 'Pre-subdomain wildcard'
        elif host+'.tk' in make_request(url, host+'.tk'):
            return 'Post-domain wildcard'
        elif 'null' == make_request(url, 'null').lower():
            return 'Null misconfiguration'

def make_request(url, origin, ssltest=False, firstrun=False):
    url = ('http://' if not (ssltest) else 'https://') + url
    if origin != 'null':
        origin = ('http://' if (ssltest) else 'https://') + origin
    response = requests.get(url, headers={'Origin': origin, 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'})
    acao, acac = False, False
    if 'Access-Control-Allow-Origin' in response.headers:
        acao = response.headers['Access-Control-Allow-Origin']
        acac = str(response.headers['Access-Control-Allow-Credentials']).lower() == 'true'
    vary = False
    if 'Vary' in response.headers:
        if 'Origin' in response.headers['Vary']:
            vary = True
    if firstrun:
        if not acac:
            acao = 'no_acac'
    if ssltest and response.headers['Strict-Transport-Security']:
        acao = ''
    return (acao or '') if acac else ''

def sld(host):
    for tld in tlds.tlds:
        if host.endswith('.' + tld):
            host = host[:-len(tld)]
    if host.count('.') == 1:
        return True