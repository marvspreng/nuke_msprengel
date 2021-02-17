#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: No Samples
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('samples').setValue(0)
    i.knob('renderSamples').setValue(0)