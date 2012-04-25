
a = '''
#include <iostream>
int main()
{
    std::cout << "Hello\";
    return 0;
}
'''

print ''.join([l + '\n' if l.startswith('#') else l.strip().split(' ') for l in a.splitlines()])
