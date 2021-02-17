#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: create Read
# COLOR: #565424
#
#----------------------------------------------------------------------------------------------------------

for w in nuke.selectedNodes():
    r = nuke.createNode('Read')
    r.knob('file').setValue(w.knob('file').getValue())
    r.knob('first').setValue(int(nuke.root().knob('first_frame').getValue()))
    r.knob('last').setValue(int(nuke.root().knob('last_frame').getValue()))
    r.knob('origfirst').setValue(int(nuke.root().knob('first_frame').getValue()))
    r.knob('origlast').setValue(int(nuke.root().knob('last_frame').getValue()))
    r.knob('colorspace').setValue(int(w.knob('colorspace').getValue()))
    