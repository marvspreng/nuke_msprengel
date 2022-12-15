#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Rename Connector
#
#----------------------------------------------------------------------------------------------------------

selection = nuke.selectedNodes()

if len(selection) == 1:
    n = selection[0]
    if "Connector" in n.name():
        txt = nuke.getInput('Change label', 'new label')

        if txt:
            n['label'].setValue(txt.upper())
            for x in n.dependent():
                x['label'].setValue(txt.upper())