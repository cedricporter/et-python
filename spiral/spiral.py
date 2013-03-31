#!/usr/bin/env python
import pprint, math, functools

def pp(func):
    @functools.wraps(func)
    def wrapper(arr, n):
        func(arr, n)
        print '\n', '-' * 10
    return wrapper

@pp
def print_arr(arr, n):
    for i in xrange(n * n):
        print '%3d' % arr[i],
        if (i + 1) % n == 0:
            print

n = 5
arr = [[0] * n for i in xrange(n)]

dx, dy = 0, 1

num = 1
for i in range(n):
    for j in range(n):
        arr[i][j] = num
        num += 1

a = [0] * (n * n)
x, y = 0, 0
for i in xrange(n * n):
    a[x * n + y] = i
    if y == n - 1:
        dx, dy = 1, 0
    elif x == n - 1:
        dx, dy = -1, 0
    x, y = x + dx, y + dy

    print_arr(a, n)

