#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: check for Versions
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    b = i.knob('checkVersions')
    b.execute()