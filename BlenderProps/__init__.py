# Blender Property generator
# Generates predefined properties to be used in conjunction with the Blenderer Add-on

from vcApplication import * #type:ignore


def OnStart():
    cmduri = getApplicationPath() + 'BlenderProps.py' #type:ignore
    cmd = loadCommand('BlenderProps', cmduri) #type:ignore
    addMenuItem(VC_MENU_MODELING_WIZARDS + '/Other', 'Blender Property Generator', -1, 'BlenderProps', 'BlenderProps', getCommandPath() + 'rBlendererIcon.svg') #type:ignore