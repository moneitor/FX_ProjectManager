import xml.etree.ElementTree as ET
node = hou.node('/currently/selected/node/path')
definition = node.type().definition()
toolssection = definitions.sections()['Tools.shelf']

root = ET.fromstring(toolssection.contents())
for path in root.iter('toolSubmenu'):
    print(path.text)
