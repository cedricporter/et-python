declaration = r'''
file           :=  [ \t\n]*, section+
section        :=  '[', section_name, ']', ts,'\n', body
section_name   :=  identifier
body           :=  statement*
statement      :=  (ts,'#', -'\n'*,'\n')/equality/nullline
nullline       :=  ts,'\n'
equality       :=  ts, item, ts, '=', ts, value, ts, '\n'
item           := identifier
identifier     :=  [a-zA-Z], [a-zA-Z0-9_]*
value          :=  -'\n'*
ts             :=  [ \t]*
'''

text = '''
[Bootstrap]
Zip=../media/packs/OgreCore.zip

# Resource locations to be added to the default path
[General]
FileSystem=../media
FileSystem=../media/Audio
FileSystem=../media/sounds
FileSystem=../media/materials/programs
FileSystem=../media/materials/scripts
FileSystem=../media/materials/textures
FileSystem=../media/models
FileSystem=../media/overlays
Zip=../media/packs/ogretestmap.zip
#Zip=../media/packs/chiropteraDM.pk3

'''
from simpleparse.parser import Parser
import pprint

lastItem = None
section_name = ''
def config_maker(tag, start, end):
    '''make the config tuple, and adds them to config'''
    global config, text, lastItem, section_name
    if tag == 'section_name':
        section_name = text[start:end]
    elif tag == 'item':
        lastItem = text[start:end]
    elif tag == 'value':
        config.append((lastItem, text[start:end]))

def travel(root, func):
    if root == None: return

    tag, start, end, children = root
    func(tag, start, end)

    if children != None:
        for item in children: travel(item, func)

if __name__ =="__main__":
    parser = Parser( declaration, "file" )
    success, resultTrees, nextChar = parser.parse(text)

    output = {}
    for section in resultTrees:
        config = []
        travel(section, config_maker)
        output[section_name] = config

    pprint.pprint(output)

