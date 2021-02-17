##Hagbarth Tools
#GIFWRITER
import gifwriter_ui

#QuickCreate
import h_viewerShortcuts

#Gradienteditor
import ColorGradientUi

toolbar = nuke.menu("Nodes")
m = toolbar.addMenu("murph/Hagbarth Tools", icon="hagbarth.png")
m.addCommand("GifWriter", "nuke.createNode(\"GifWriter\")")
m.addCommand("LUEGRADE", "nuke.createNode(\"LUEGRADE\")")
m.addCommand("Gradienteditor", "nuke.createNode(\"h_gradienteditor\")", icon="h_gradienteditor.png")
