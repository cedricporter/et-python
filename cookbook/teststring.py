#!/usr/bin/env python
import string

allchars = string.maketrans('', '')

def makefilter(keep):
    delchars = allchars.translate(allchars, keep)
    def thefilter(s):
        return s.translate(allchars, delchars)
    return thefilter

if __name__ == '__main__':
    t_filter = makefilter('abcdef')
    print t_filter('hello, et')

