#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: add enableOnRender
# COLOR: #524641
#
#----------------------------------------------------------------------------------------------------------

nodes = nuke.selectedNodes()

for n in nodes:

    str = n.knob('label').getValue()
    
    if n.Class() != ('Dot') and n.Class() != ('BackdropNode'):
        if "enableOnRender" not in str:
            if str == '':
                n.knob('label').setValue(str + r'enableOnRender')    
            else:
                n.knob('label').setValue(str + r' \n enableOnRender')