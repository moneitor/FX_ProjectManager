node = hou.selectedNodes()[0]
df = node.type().definition()
sections = df.sections()

for name, value in sections.items():
  print(name)
  
toolssection = sections()['Tools.shelf']
