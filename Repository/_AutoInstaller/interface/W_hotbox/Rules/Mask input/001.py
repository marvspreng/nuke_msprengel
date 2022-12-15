#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Mask invert
# COLOR: #009fff
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('invert_mask').getValue() == True:
        i.knob('invert_mask').setValue(False)
    else:
        i.knob('invert_mask').setValue(True)