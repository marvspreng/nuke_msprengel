#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: make Connector
#
#----------------------------------------------------------------------------------------------------------

selection = nuke.selectedNodes()
  

for d in selection:

    name = d.knob('name').getValue()
    d.knob('name').setValue('rename')
    newname = name.replace('Dot','Connector') 
    nameexist = 0
    for x in nuke.allNodes('Dot'):
        if newname == x.name():
            nameexist = 1
      
    while nameexist == 1:
        nameexist = 0
        newname = newname+'1'
        for x in nuke.allNodes('Dot'):
            if newname == x.name():
                nameexist = 1
                
    d.knob('name').setValue(newname)     
    d.knob('note_font_size').setValue(44)       
    

if len(selection) == 1:
    txt = False
    d = nuke.selectedNode()
    if d['label'].getValue() is "":    
        txt = nuke.getInput('Change label', 'new label')
    else:
        txt = nuke.getInput('Change label', d['label'].getValue())
        
    if txt:
       d['label'].setValue(txt.upper())  
