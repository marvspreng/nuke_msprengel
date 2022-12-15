##Hagbarth Tools
#GIFWRITER
import gifwriter_ui

#QuickCreate
import h_viewerShortcuts

toolbar = nuke.menu("Nodes")
m = toolbar.addMenu("murph/Hagbarth Tools", icon="hagbarth.png")
m.addCommand("GifWriter", "nuke.createNode(\"GifWriter\")")
