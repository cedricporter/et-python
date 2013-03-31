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

from spark import GenericParser, GenericScanner

class Token(object):
    def __init__(self, type, attr=''):
        self.type = type
        self.attr = attr
    def __cmp__(self, o):
        return cmp(self.type, o)
    def __str__(self):
        return self.type
    def __repr__(self):
        return str(self)

class SimpleScanner(GenericScanner, object):
    def __init__(self):
        GenericScanner.__init__(self)

    def tokenize(self, input):
        self.rv = []
        GenericScanner.tokenize(self, input)
        return self.rv

    def t_whitespace(self, s):
        r' \s+ '
        pass

    def t_op(self, s):
        r' \+ | \- | \* | / | \( | \) '
        self.rv.append(Token(type=s))

    def t_number(self, s):
        r' \d+ '
        self.rv.append(Token(type='number', attr=s))

class ExprParser(GenericParser):
    def __init__(self, start='expr'):
        GenericParser.__init__(self, start)

    def p_expr_term_0(self, (lhs, op, rhs)):
        '''
            expr ::= expr addop term 
            term ::= term mulop factor
        '''
        return eval(str(lhs) + str(op) + str(rhs))

    def p_expr_term_factor_1(self, (v, )):
        '''
            expr ::= term
            term ::= factor
        '''
        return v

    def p_factor_1(self, (n, )):
        ' factor ::= number '
        return int(n.attr)

    def p_factor_2(self, (_0, expr, _1)):
        ' factor ::= ( expr ) '
        return expr

    def p_addop_mulop(self, (op, )):
        ''' 
            addop ::= +
            addop ::= -
            mulop ::= *
            mulop ::= /
        '''
        return op


def scan(code):
    scanner = SimpleScanner()
    return scanner.tokenize(code)

def parse(tokens):
    parser = ExprParser()
    return parser.parse(tokens)

if __name__ == '__main__':
    text = ' 7 + (1 + 3) * 5'
    print parse(scan(text))
    
