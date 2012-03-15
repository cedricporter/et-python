#!/usr/bin/env python
import re
import pprint
from simpleparse.parser import Parser
from simpleparse import dispatchprocessor

declaration = r'''
file            := [ \t\r\n]*, grammer+
grammer         := header, ts, '->', ts, blocks
ts              := [ \t]*
header          := identifier
identifier      := [a-zA-Z_]+
blocks          := block, [\r\n]*, (ts, "|", ts, block, [ \r\n]*)*
block           := -[|\r\n]+
'''

maxTagLen = -1
def counter(tag, start, end):
    '''Find the longest length of header'''
    global maxTagLen
    if tag == 'header' and maxTagLen < end - start:
        maxTagLen = end - start

isFisrtBlock = True 
offset = -1
def printer(tag, start, end):
    '''print the grammers'''
    global text, isFisrtBlock, maxTagLen, offset
    if tag == 'header':
        offset = maxTagLen - (end - start)
        print text[start:end],
    elif tag == 'blocks':
        print offset * ' ', '->',
        isFisrtBlock = True
    elif tag == 'block':
        print "%s%s" % ('' if isFisrtBlock else (maxTagLen + 3) * ' ' + '| ', text[start:end])
        isFisrtBlock = False

def travel(root, func):
    if root == None: return

    tag, start, end, children = root
    func(tag, start, end)

    if children != None:
        for item in children: travel(item, func)

if __name__ =="__main__":
    inFile = open("2.txt")
    text = ""
    for line in inFile.readlines():
        text += line + "\n"

    parser = Parser( declaration, "file" )
    success, resultTrees, nextChar = parser.parse(text)
    #pprint.pprint(resultTrees) 

    for item in resultTrees: travel(item, counter)
    print maxTagLen
    for item in resultTrees: travel(item, printer)
    

