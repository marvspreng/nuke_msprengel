#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Position
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if 'Position' in nuke.channels():
        i.knob('in').setValue('Position')
        print "testauch"
    else:
        i.knob('in').setValue('Position')
        print "test"
    i.knob('tile_color').setValue(2130739199)