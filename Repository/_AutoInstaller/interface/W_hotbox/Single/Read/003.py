#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Set Project Format
#
#----------------------------------------------------------------------------------------------------------

node = nuke.selectedNode()
format = node.knob('format').value()
nuke.Root().knob('format').setValue(format)