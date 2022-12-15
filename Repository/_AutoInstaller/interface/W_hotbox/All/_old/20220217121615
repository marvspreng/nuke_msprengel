#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: disable all enableOnRender
# COLOR: #524a3b
#
#----------------------------------------------------------------------------------------------------------

import nuke

nodes = nuke.allNodes()

for n in nodes:

    str = n.knob('label').getValue()

    if "enableOnRender" in str:
        n.knob('disable').setValue(True)
        