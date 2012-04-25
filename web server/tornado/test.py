class A(object):
    def __init__(self, i):
        self.__i = i
        self.__x = i

    def get_i(self):
        return self.__i

    def set_i(self, i):
        self.__i = i * 2
    i = property(get_i, set_i, doc='Hello, ET')

    @property
    def x():
        def fget(self):
            return self.__x * -1
        def fset(self, x):
            self.__x = x * 2
        #print locals()
        return locals()



if False and __name__ == '__main__': 
    a = A(5)
    b = A(5)
    print dir(a)
    #print 'a.x', a.x
    a.x = 3
    print 'a.x', a.x
    print A.i.__doc__
    print 'a.i', a.i
    print 'b.i', b.i
    a.i = 7
    b.set_i(7)
    print 'a.i', a.i
    print 'b.i', b.i

