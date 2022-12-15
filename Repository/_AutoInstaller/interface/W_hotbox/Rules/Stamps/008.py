#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: zoom anchor
#
#----------------------------------------------------------------------------------------------------------

ns = [n for n in nuke.selectedNodes() if n.knob("identifier")]
for n in ns:
    try:
        n["zoom_anchor"].execute()
    except:
        pass