#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Black
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('in').setValue('rgba')
    for channel in ['red','green','blue','alpha']:
        i.knob(channel).setValue('black')

#    i.knob('tile_color').setValue(421934079)