import os, re

os.setuid(33)

def get_uid(username = 'www-data'):
    pwd = open('/etc/passwd', 'r')
    pat = re.compile(username + ':.*?:(.*?):.*?')
    for line in pwd.readlines():
        try:
            uid = pat.search(line).group(1)
        except: continue
        return int(uid)

print get_uid()


