
a = '''
#include <iostream>
int main()
{
    std::cout << "Hello\";
    return 0;
}
'''

print ''.join([l + '\n' if len(l) and l[0] == '#' else l.strip() for l in a.splitlines()])
