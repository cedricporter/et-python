s = 'Hello, ET'

print s[::-1]

print ''.join([s[i] for i in range(len(s) - 1, -1, -1)])

print ''.join(reversed(s)) 

new_s = list(s)
new_s.reverse()
print ''.join(new_s)

new_s = ''
for i in s:
    new_s = i + new_s
print new_s

new_s = ''
for i in range(len(s)):
    new_s = s[i] + new_s
print new_s

# generator
def r(s):
    while len(s):
        yield s[-1]
        s = s[:-1]
print ''.join(r(s))

# so called functional programming
def r1(s):
    if not len(s) : return s
    return s[-1] + r1(s[:-1])
print r1(s)


