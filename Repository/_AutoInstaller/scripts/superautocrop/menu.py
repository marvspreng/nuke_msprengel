import superAutoCrop

#Add a menu and assign a shortcut
toolbar = nuke.menu('Nuke')
cqnTools = toolbar.addMenu('Marv')
cqnTools.addCommand('superAutoCrop', 'superAutoCrop.superAutoCrop()', '[', icon='AutoCrop.png')