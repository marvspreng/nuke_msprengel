#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Copy UNC Path
#
#----------------------------------------------------------------------------------------------------------

import os
from Qt import QtWidgets

clipboard = QtWidgets.QApplication.clipboard()

for i in nuke.selectedNodes():
    x = os.path.dirname(i['file'].getValue())+'/'
    clipboard.setText(x.replace('/','\\'))