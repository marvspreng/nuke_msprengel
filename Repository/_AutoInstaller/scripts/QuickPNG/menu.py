

menubar = nuke.menu('Nuke')
menubar.addMenu('Marv')
menubar.addCommand("@;QuickPNG", "nuke.load('QuickPNG')", 'alt+r') #instantly write a PNG at the selected node to the desktop when pressing alt + r