#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Set Passes
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('P_channel').setValue('WSC')
    i.knob('N_channel').setValue('WNormals')