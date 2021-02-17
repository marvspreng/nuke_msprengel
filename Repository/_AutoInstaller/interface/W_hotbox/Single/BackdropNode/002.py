#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Font Size
#
#----------------------------------------------------------------------------------------------------------

txt = nuke.getInput('Change Font Size', '50')
if txt:
    for n in nuke.selectedNodes():
        txt = int(txt)
        n['note_font_size'].setValue(txt)
                