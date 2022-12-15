#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: disable all PostageStamps
# COLOR: #4c4352
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.allNodes():
    if "postage_stamp" in node.knobs():
        node["postage_stamp"].setValue(False)