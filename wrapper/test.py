import copy

def freshdefaults(f):
    fdefaults = f.func_defaults
    def refresher(*args, **kwds):
        f.func_defaults = copy.deepcopy(fdefaults)
        return f(*args, **kwds)
    return refresher

@freshdefaults
def packitem(item, pkg = []):
    pkg.append(item)
    return pkg

l = [100,200]
packitem(300, l)
packitem(1)
packitem(2)
packitem(3)
    

class Rectange(object):
    def __init(self, x, y):
        """Initliaze the func
        
        Arguments:
        - `x`:
        - `y`:
        """
        self.x = x
        self.y = y
    def area():
        doc = "sb"
        def fget(self):
            print 'in area get'
            return self.x * self.y
        def fset(self, value):
            print 'in area set'
            self.x = int(value[0])
            self.y = int(value[1])
        return locals()
    area = property(**area())

rect = Rectange()

        
