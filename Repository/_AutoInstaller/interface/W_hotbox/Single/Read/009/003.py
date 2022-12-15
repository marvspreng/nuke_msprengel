#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Replace Read
#
#----------------------------------------------------------------------------------------------------------

import os

for i in nuke.selectedNodes():
    x = nuke.getClipname('Replace', '', os.path.dirname(i['file'].getValue())+'/')
    if x != None:
        
        file = x.split(' ')
        frame = file[1].split('-')
        i['file'].setValue(file[0])
        i['first'].setValue(int(frame[0]))
        i['last'].setValue(int(frame[1]))
        i['origfirst'].setValue(int(frame[0]))
        i['origlast'].setValue(int(frame[1]))

    