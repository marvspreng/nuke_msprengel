#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Label
#
#----------------------------------------------------------------------------------------------------------

txt = nuke.getInput('Change label', 'Enter Name')
if txt:
    for n in nuke.selectedNodes():
        n['label'].setValue(txt.upper())
                
        
            

    
    