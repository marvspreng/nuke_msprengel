#convert FBX, ABC, etc directly to their related node (ReadGeo, etc.)
import convert
nuke.menu("Nuke").addCommand("Marv/convert/convert file node (guess)", lambda: convert.show_convert_node_panel(guess=True))
nuke.menu("Nuke").addCommand("Marv/convert/convert file node (manual)", convert.show_convert_node_panel)
