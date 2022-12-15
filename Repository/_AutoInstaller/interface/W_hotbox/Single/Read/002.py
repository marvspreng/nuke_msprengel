#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: show/hide PostageStamp
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():

    stamp = i.knob('postage_stamp')
    if stamp.getValue() == 0:
        stamp.setValue(1)
    else:
        stamp.setValue(0)