from preferences import Preferences
import nuke

def addMenus():
    #ADD SHARETOOLFROMDAG OPTION TO NUKE MENU
    shortcuts = nuke.menu("Nodes").menu("ToolSets").addMenu("NodeBoard")
    shortcuts.addCommand("ShareToolFromDAG", 'sharetoolfromdag.shareToolFromDAG()', shareShortcut())
    shortcuts.addCommand("GetToolToDAG", 'sharetoolfromdag.getToolToDAG()', getShortcut())

def resetShortcuts():
    Preferences().savePreferencesToFile()
    editMenu = nuke.menu("Nodes").menu("ToolSets")
    if editMenu.findItem('NodeBoard'):
        print('changing')
        editMenu.menu('NodeBoard').removeItem('ShareToolFromDAG')
        editMenu.menu('NodeBoard').removeItem('GetToolToDAG')
    addMenus()

def shareToolFromDAG():
    print('sharing')
    preferences = Preferences()
    shareLocation = preferences.preferencesNode.knob('nodeboardShareLocation').value()
    name = 'shareToolFromDAG_file'
    ext = '.nk'
    path = shareLocation
    if path == '':
        nuke.message('Please specify the save location in the Preferences-Nodeboard first!')

    else:
        tool = nuke.selectedNodes()
        if tool == None:
            nuke.message('no nodes selected')
        else:            
            nuke.nodeCopy(path + name + ext)

def getToolToDAG():
    print('getting')
    preferences = Preferences()
    shareLocation = preferences.preferencesNode.knob('nodeboardShareLocation').value()

    name = 'shareToolFromDAG_file'
    ext = '.nk'
    path = shareLocation
    try:
        nuke.nodePaste(path + name + ext)
    except RuntimeError:
        nuke.message('Server location is empty')

def shareShortcut():
    preferences = Preferences()
    try:
        shortcut = preferences.preferencesNode.knob('nodeboardShareShortcut').value()
        return shortcut
    except:
        return 'Ctrl+Alt+C'

def getShortcut():
    preferences = Preferences()
    try:
        shortcut = preferences.preferencesNode.knob('nodeboardGetShortcut').value()
        return shortcut
    except:
        return 'Ctrl+Alt+V'




