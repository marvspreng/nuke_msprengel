#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Premult
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('premultiply').getValue() == 1.0:
        i.knob('premultiply').setValue('none')
    elif i.knob('premultiply').getValue() == 0.0:
        i.knob('premultiply').setValue('rgba')
