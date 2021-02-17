#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Relink
# COLOR: #9e1f00
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    txt = nuke.getInput('Enter Name of Stabilize Node', 'Transform_Stabilize')
    i.knob('StabNode').setValue(txt)
    