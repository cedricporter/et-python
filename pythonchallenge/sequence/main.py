import re


def read(num):
    pat = re.compile(r'(1+|2+|3+)')
    return ''.join(str(len(i)) + i[0] for i in pat.findall(num))

num = '1'
for i in range(30):
    num = read(num)
    print num

print len(num)
    
