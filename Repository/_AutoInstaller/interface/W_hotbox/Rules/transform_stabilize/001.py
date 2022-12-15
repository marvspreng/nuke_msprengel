#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Rename
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    txt = nuke.getInput('Enter Node Name','Transform_Stabilize')
    i.knob('name').setValue(txt)