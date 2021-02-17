#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Set Frame
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('referenceFrame').setValue(nuke.frame())
