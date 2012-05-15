#!/usr/bin/env python
# author:  Hua Liang [ Stupid ET ]
# email:   et@everet.org
# website: http://EverET.org
#

# Grammar:
#     expr    ::= expr addop term | term
#     term    ::= term mulop factor | factor
#     factor  ::= number | ( expr )
#     addop   ::= + | -
#     mulop   ::= * | /

import tokenize, StringIO

tokens = None
cur_tok = None

def scan(text):
    g = tokenize.generate_tokens(
        StringIO.StringIO(text).readline)
    return ((v[0], v[1]) for v in g)
    
def get_token():
    global tokens, cur_tok
    cur_tok = tokens.next()
    #print cur_tok
    return cur_tok
    
def match(type, val = ''):
    global tokens, cur_tok
    t, v = cur_tok
    if t == type or t == tokenize.OP and v == val:
        get_token()
    else:
        raise 

def expr():
    global cur_tok
    tmp = term()
    t, v = cur_tok
    while v == '+' or v == '-':
        match(tokenize.OP)
        rhs = term()
        e = str(tmp) + str(v) + str(rhs)
        tmp = eval(e)
        print e, '=', tmp
        t, v = cur_tok
    return tmp 

def term():
    global cur_tok
    tmp = factor()
    t, v = cur_tok
    while v == '*' or v == '/':
        match(tokenize.OP)
        rhs = factor()
        e = str(tmp) + str(v) + str(rhs)
        tmp = eval(e)
        print e, '=', tmp
        t, v = cur_tok
    return tmp

def factor():
    global cur_tok
    t, v = cur_tok
    if t == tokenize.NUMBER:
        match(tokenize.NUMBER)
        return int(v)
    elif v == '(':
        match(tokenize.OP, '(')
        tmp = expr()
        match(tokenize.OP, ')')
        return tmp
    else:
        raise

if __name__ == '__main__':
    text = '12 + 2 * ( 5 + 6 )'
    tokens = scan(text)
    get_token()
    res = expr()
    print text, '=', res
