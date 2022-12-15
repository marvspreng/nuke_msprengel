#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: hide Viewer lines
#
#----------------------------------------------------------------------------------------------------------


for i in nuke.allNodes('Viewer'):

    i.knob('hide_input').setValue(1)