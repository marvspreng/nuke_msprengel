#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: toggle Postage Stamp
# COLOR: #4c4352
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    
    toggleClasses = 'Cryptomatte Shuffle P_Matte Roto P_Ramp PostageStamp Keyer Read'
    
    if i.Class() in toggleClasses or i.name() in toggleClasses:
        stamp = i.knob('postage_stamp')
        if stamp.getValue() == 0:
            stamp.setValue(1)
        else:
            stamp.setValue(0)