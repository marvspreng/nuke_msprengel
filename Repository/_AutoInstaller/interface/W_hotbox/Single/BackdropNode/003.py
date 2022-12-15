#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Color
#
#----------------------------------------------------------------------------------------------------------

col = nuke.getColor()

if col:
    for n in nuke.selectedNodes():
        n['tile_color'].setValue(col)
        n['gl_color'].setValue(col)