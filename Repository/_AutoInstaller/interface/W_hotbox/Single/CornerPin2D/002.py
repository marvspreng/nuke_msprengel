#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Break "from" animation
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('from1').clearAnimated()
    i.knob('from2').clearAnimated()
    i.knob('from3').clearAnimated()
    i.knob('from4').clearAnimated()
    i.knob('label').setValue('Stab Frame : ' + str(nuke.frame()))
    