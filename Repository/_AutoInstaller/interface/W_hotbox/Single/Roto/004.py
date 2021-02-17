#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Replace
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('replace').getValue() == False:
        i.knob('replace').setValue(True)
    else:
        i.knob('replace').setValue(False)
    
        