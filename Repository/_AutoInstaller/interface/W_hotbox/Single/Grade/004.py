#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Mask Grade
# COLOR: #7f0100
#
#----------------------------------------------------------------------------------------------------------

for n in nuke.selectedNodes():
    n.knob('white').setValue(0)
    n.knob('channels').setValue('rgba')