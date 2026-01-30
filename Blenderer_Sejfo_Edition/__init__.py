from vcApplication import *

cmdName = 'cmdBlenderer2'
title = 'Blenderer 2'
pyNetCommand = findCommand('netCommand')
pyNetCommand.execute('SetLocalizationCommand', 'English', 'Python', cmdName, 'Text', title)

def OnStart():
  cmduri = getApplicationPath() + 'Blenderer.py'
  cmd = loadCommand(cmdName, cmduri)
  iconuri = getCommandPath() + 'rBlendererIcon.svg'
  addMenuItem('VcTabHome/Render', title, -1, cmdName, iconuri)
  addMenuItem('VcTabAuthor/Render', title, -1, cmdName, iconuri)

