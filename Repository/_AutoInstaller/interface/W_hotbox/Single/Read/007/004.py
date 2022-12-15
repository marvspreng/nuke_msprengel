#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Linear
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('colorspace').setValue('linear')