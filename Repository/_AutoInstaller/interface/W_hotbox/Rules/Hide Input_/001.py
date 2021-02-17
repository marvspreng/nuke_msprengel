#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Hide Input
# COLOR: #990000
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('hide_input').getValue() == True:
        i.knob('hide_input').setValue(False)
    else:
        i.knob('hide_input').setValue(True)