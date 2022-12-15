#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Start at Project
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('frame_mode').setValue("start at")
    i.knob('frame').setValue(nuke.Root().knob('first_frame'))