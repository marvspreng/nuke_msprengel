#coding: utf-8

###################

# viewer lock v1.7
#    - no changes to this file in this update, only a change to the menu.py to add shortcutContext=2 to the "connect" hotkeys in order to better match default nuke behaviour (thanks james rowell for pointing this out!)

# to do:
#    - viewer lock is long overdue a big code refactor and bug fix update
#    - in particular need to investigate a report of crashing on script open, might be due to the EXTREMELY dodgy panel registration code in the menu.py

# please enjoy
# love, matt

##################

import nuke
import nukescripts
import os
directory = os.path.dirname(os.path.abspath(__file__))

try:
    #nuke <11
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtGui as QtGuiWidgets

except:
    #nuke>=11
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtGuiWidgets


#########
# LOGIC #
#########

#necessary to prevent nuke callbacks from interfering with certain processes
class processes(object):

    def __init__(self):
        self.viewerProcess = False
        self.guiProcess = False
    def check(self):
        if self.viewerProcess == False and self.guiProcess == False:
            return False
        else:
            return True

procs = processes()

#viewer object to keep track of inputs and lock states
class Viewer(object):

    def __init__(self, node):
        self.node = node
        self.input = []
        self.targetList = [None, None, None, None, None, None, None, None, None, None]

        #add boolean knobs to viewer node for input lock states if it doesn"t have them
        procs.viewerProcess = True
        if not "viewerLockInputStates" in self.node.knobs():
            tab = nuke.Tab_Knob("viewerLockInputStates")
            tab.setFlag(nuke.INVISIBLE)
            tab.setFlag(nuke.DONT_SAVE_TO_NODEPRESET)
            self.node.addKnob(tab)

            self.node.addKnob(nuke.Text_Knob("READ_ME"))
            self.node["READ_ME"].setFlag(nuke.DONT_SAVE_TO_NODEPRESET)
            self.node["READ_ME"].setFlag(nuke.INVISIBLE)
            self.node["READ_ME"].setValue("""The following knobs are needed for the Viewer Lock
plugin to function. If you don"t have Viewer Lock,
you can safely ignore or delete them.

If they"re causing problems, let me know at
matt_roe@live.com.
""")

            for x in range(10):
                knob = nuke.Boolean_Knob("inputState%s" %x)
                knob.setFlag(nuke.STARTLINE)
                knob.setFlag(nuke.NO_ANIMATION)
                knob.setFlag(nuke.DONT_SAVE_TO_NODEPRESET)
                knob.setFlag(nuke.NO_UNDO)
                knob.setFlag(nuke.INVISIBLE)
                self.node.addKnob(knob)

        #initialise target list
        for x in range(10):
            if self.isLocked(x):
                self.targetList[x] = self.node.input(x)
        procs.viewerProcess = False

    def isLocked(self, x):
        return bool(self.node["inputState%s" %x].getValue())

    def setLocked(self, x, state, switchTo=True):
        procs.viewerProcess = True
        if state == True:
            if switchTo == True:
                nukescripts.connect_selected_to_viewer(x)
            self.targetList[x] = self.node.input(x)
        if state == False:
            if switchTo == True:
                nukescripts.connect_selected_to_viewer(x)
            self.targetList[x] = None
        self.node["inputState%s" %x].setValue(state)
        procs.viewerProcess = False

    def inputTarget(self, x):
        return self.targetList[x]


viewerList = {}

def attemptUpdateUI():
    if "vLPanel" in locals() or "vLPanel" in globals():
        vLPanel.viewerLockKnob.getObject().viewerMenuWidget.updateUI()

def updateViewerList():
    if not nuke.activeViewer() == None:
        v = nuke.activeViewer().node()
        #add new viewers to the viewerList dictionary:
        if not v in viewerList:
            viewerList[v]=Viewer(v)
        #set all locked inputs to their targets:
        for x in range(10):
            if procs.check() == False:
                if viewerList[v].isLocked(x) == True:
                    try:
                        v.setInput(x, viewerList[v].inputTarget(x))
                    except:
                        viewerList[v].setLocked(x, False)
                        v.setInput(x, None)

#unlocks all inputs of viewer in use
def unlockAll():
    updateViewerList()
    if not nuke.activeViewer() == None:
        for x in range(10):
            viewerList[nuke.activeViewer().node()].setLocked(x, False, False)
    attemptUpdateUI()

#locks all inputs of viewer in use
def lockAll():
    updateViewerList()
    if not nuke.activeViewer() == None:
        for x in range(10):
            viewerList[nuke.activeViewer().node()].setLocked(x, True, False)
    attemptUpdateUI()

#returns true if the active viewer is within current DAG context
def checkDAGContext():
    updateViewerList()
    if nuke.activeViewer() == None:
        return False
    else:
        activeViewerGroup = nuke.activeViewer().node().fullName().split(".")[:-1]
        if len(activeViewerGroup) > 0:
            activeViewerContext = "root."+".".join(activeViewerGroup)
        else:
            activeViewerContext = "root"
        if not nuke.thisGroup().fullName() == "root":
            dagContext = "root."+nuke.thisGroup().fullName()
        else:
            dagContext = "root"
        if nuke.toNode(activeViewerContext) == nuke.toNode(dagContext):
            return True
        else:
            return False

#checks if a viewer is locked and sets viewer input based on that
def connect(input):
    updateViewerList()
    if checkDAGContext() == True:
        if viewerList[nuke.activeViewer().node()].isLocked(input) == True:
            if viewerList[nuke.activeViewer().node()].inputTarget(input) == None:
                pass
            else:
                nuke.activeViewer().activateInput(input)
        else:
            nukescripts.connect_selected_to_viewer(input)
    else:
        nukescripts.connect_selected_to_viewer(input)
    attemptUpdateUI()

#neater way of locking
def lock(input, switchTo=True):
    if nuke.activeViewer() == None:
        nukescripts.connect_selected_to_viewer(input)
    updateViewerList()
    viewerList[nuke.activeViewer().node()].setLocked(input, True, switchTo)
    attemptUpdateUI()

#neater way of unlocking
def unlock(input, switchTo=True):
    if nuke.activeViewer() == None:
        nukescripts.connect_selected_to_viewer(input)
    updateViewerList()
    viewerList[nuke.activeViewer().node()].setLocked(input, False, switchTo)
    attemptUpdateUI()



#######
# GUI #
#######

#a label which shrinks to fit windows
class elidedLabel(QtGuiWidgets.QLabel):
    def __init__(self, parent=None):
        super(elidedLabel, self).__init__(parent)
    def paintEvent(self, event):
        elided = QtGui.QFontMetrics(self.font()).elidedText(self.text(), QtCore.Qt.ElideRight, self.width())
        QtGui.QPainter(self).drawText(self.rect(), self.alignment(), elided)


#delete checkboxes
class deleteCheckBox(QtGuiWidgets.QCheckBox):

    def __init__(self, x, guiObj):
        super(deleteCheckBox, self).__init__()
        self.index = x
        self.guiObj = guiObj
        self.setStyleSheet("background:transparent")
        self.setEnabled(False)
        self.stateChanged.connect(self.deleteInput)

    def deleteInput(self):
        if not self.guiObj.active == None:
            v = self.guiObj.viewerList[self.guiObj.active.node()]
            v.setLocked(self.index, False, False)
            v.node.setInput(self.index, None)
            self.guiObj.updateUI()


#toggle checkboxes
class toggleCheckBox(QtGuiWidgets.QCheckBox):

    def __init__(self, x, guiObj):
        super(toggleCheckBox, self).__init__()
        self.index = x
        self.guiObj = guiObj
        self.setText(str(x+1)[-1:])
        self.stateChanged.connect(self.lockToggle)

    def lockToggle(self):
        procs.guiProcess = True
        if self.guiObj.inputToggleList[self.index].isChecked():
            lock(self.index, False)
        else:
            unlock(self.index, False)
        procs.guiProcess = False
        self.guiObj.updateUI()

#GUI wrapper
class viewerMenu(QtGuiWidgets.QWidget):

    def __init__(self, viewerListObj, parent=None):
        super(viewerMenu, self).__init__()

        self.viewerList = viewerListObj
        self.setLayout(QtGuiWidgets.QVBoxLayout())
        self.layout().setSpacing(5)
        self.setMaximumHeight(450)
        self.active = None

        self.viewerSpacer = QtGuiWidgets.QSpacerItem(10, 10)
        self.layout().addItem(self.viewerSpacer)

        self.deleteAllIcon = QtGuiWidgets.QLabel()
        self.deleteAllIcon.setPixmap(QtGui.QPixmap("%s/viewerlock_input.png" %directory))
        self.deleteAllCheckBox = QtGuiWidgets.QCheckBox()
        self.deleteAllCheckBox.stateChanged.connect(self.deleteAll)
        self.deleteAllCheckBox.setEnabled(False)
        self.deleteAllCheckBox.setStyleSheet("background:transparent")
        self.deleteAllLayout = QtGuiWidgets.QVBoxLayout()
        self.deleteAllLayout.setSpacing(2)
        self.deleteAllLayout.addWidget(self.deleteAllIcon)
        self.deleteAllLayout.addWidget(self.deleteAllCheckBox)

        self.toggleAllIcon = QtGuiWidgets.QLabel()
        self.toggleAllIcon.setPixmap(QtGui.QPixmap("%s/viewerlock_lock.png" %directory))
        self.toggleAllCheckBox = QtGuiWidgets.QCheckBox()
        self.toggleAllCheckBox.stateChanged.connect(self.toggleAll)
        self.toggleAllLayout = QtGuiWidgets.QVBoxLayout()
        self.toggleAllLayout.setSpacing(2)
        self.toggleAllLayout.addWidget(self.toggleAllIcon)
        self.toggleAllLayout.addWidget(self.toggleAllCheckBox)

        self.downArrowIcon = QtGuiWidgets.QLabel("↓")
        self.downArrowIcon.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

        self.viewerLabel = QtGuiWidgets.QLabel()
        self.viewerLabel.setStyleSheet("""
                                        color:white;
                                        font-weight:bold;
                                        """)
        self.viewerLabel.setText("No active viewer")
        self.viewerLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

        self.topLineLayout = QtGuiWidgets.QHBoxLayout()
        self.topLineLayout.setSpacing(5)
        self.topLineLayout.setContentsMargins(0,0,0,4)
        self.topLineLayout.setAlignment(QtCore.Qt.AlignLeft)

        self.topLineLayout.addLayout(self.deleteAllLayout)
        self.topLineLayout.addLayout(self.toggleAllLayout)
        self.topLineLayout.addWidget(self.downArrowIcon)
        self.topLineLayout.addWidget(self.viewerLabel)

        self.layout().addLayout(self.topLineLayout)

        self.separator = QtGuiWidgets.QFrame()
        self.separator.setFrameShape(QtGuiWidgets.QFrame.HLine)
        self.separator.setFrameShadow(QtGuiWidgets.QFrame.Sunken)
        self.layout().addWidget(self.separator, QtCore.Qt.AlignVCenter)

        self.inputDeleteList = []
        self.inputToggleList = []
        self.inputLabelList = []

        for x in range(10):
            self.inputLayout = QtGuiWidgets.QHBoxLayout()
            self.inputLayout.setSpacing(5)

            self.inputLabel = elidedLabel()
            self.inputLabel.setStyleSheet("color:grey")
            self.inputLabel.setText("—")
            self.inputLabel.setSizePolicy(QtGuiWidgets.QSizePolicy.Ignored, QtGuiWidgets.QSizePolicy.Ignored)
            self.inputLabelList.append(self.inputLabel)

            self.inputDeleteList.append(deleteCheckBox(x, self))
            self.inputToggleList.append(toggleCheckBox(x, self))

            self.inputLayout.addWidget(self.inputDeleteList[x])
            self.inputLayout.addWidget(self.inputToggleList[x])
            self.inputLayout.addWidget(self.inputLabelList[x], QtCore.Qt.AlignLeft)
            self.layout().addLayout(self.inputLayout)
        self.layout().addItem(self.viewerSpacer)

    def deleteAll(self):
        if procs.check() == False:
            if self.deleteAllCheckBox.isChecked() == False:
                for x in range(10):
                    self.viewerList[self.active.node()].setLocked(x, False, False)
                    self.active.node().setInput(x, None)
            self.deleteAllCheckBox.setEnabled(False)

    def toggleAll(self):
        self.toggleAllCheckBox.blockSignals(True)
        if self.toggleAllCheckBox.isChecked():
            lockAll()
            self.toggleAllCheckBox.setChecked(True) #failsafe
        else:
            unlockAll()
            self.toggleAllCheckBox.setChecked(False) #failsafe
        self.toggleAllCheckBox.blockSignals(False)
        self.updateUI()

    #updates the UI.
    def updateUI(self):
        self.toggleAllCheckBox.blockSignals(True)
        self.deleteAllCheckBox.blockSignals(True)
        if procs.check() == False:
            updateViewerList()
            procs.guiProcess = True
            self.toggleAllCheckBox.setChecked(False)
            self.deleteAllCheckBox.setChecked(False)
            self.deleteAllCheckBox.setEnabled(False)
            self.deleteAllCheckBox.setStyleSheet("background:transparent")
            if not nuke.activeViewer() == None:
                self.active = nuke.activeViewer()
                self.viewerLabel.setText(self.active.node().fullName())
                for x in range(10):
                    self.inputDeleteList[x].blockSignals(True)
                    self.inputToggleList[x].blockSignals(True)

                    if self.active.node().input(x) == None:
                        self.inputDeleteList[x].setChecked(False)
                        self.inputDeleteList[x].setEnabled(False)
                        self.inputDeleteList[x].setStyleSheet("background:transparent")
                    else:
                        self.deleteAllCheckBox.setChecked(True)
                        self.deleteAllCheckBox.setEnabled(True)
                        self.deleteAllCheckBox.setStyleSheet("")
                        self.inputDeleteList[x].setChecked(True)
                        self.inputDeleteList[x].setEnabled(True)
                        self.inputDeleteList[x].setStyleSheet("")

                    if self.viewerList[self.active.node()].isLocked(x) == True:
                        if self.active.activeInput() == x:
                            self.inputLabelList[x].setStyleSheet("""
                                                                font-weight:bold;
                                                                color:red;
                                                                """)
                        else:
                            self.inputLabelList[x].setStyleSheet("color:red")
                        self.toggleAllCheckBox.setChecked(True)
                        self.inputToggleList[x].setChecked(True)
                        if self.viewerList[self.active.node()].inputTarget(x) == None:
                            self.inputLabelList[x].setText("locked")
                        else:
                            self.inputLabelList[x].setText("locked to %s" % self.viewerList[self.active.node()].inputTarget(x).name())
                    else:
                        self.inputToggleList[x].setChecked(False)
                        if self.active.node().input(x) == None:
                            self.inputLabelList[x].setStyleSheet("color:grey")
                            self.inputLabelList[x].setText("—")
                        else:
                            if self.active.activeInput() == x:
                                self.inputLabelList[x].setStyleSheet("""
                                                                    font-weight:bold;
                                                                    color:lightgrey;
                                                                    """)
                            else:
                                self.inputLabelList[x].setStyleSheet("color:lightgrey")
                            self.inputLabelList[x].setText(self.active.node().input(x).name())

                    self.inputDeleteList[x].blockSignals(False)
                    self.inputToggleList[x].blockSignals(False)

            else:
                self.active = None
                self.viewerLabel.setText("No active viewer")
                for x in range(10):
                    self.inputLabelList[x].setStyleSheet("color:grey")
                    self.inputLabelList[x].setText("—")

                    self.inputToggleList[x].blockSignals(True)
                    self.inputToggleList[x].setChecked(False)
                    self.inputToggleList[x].blockSignals(False)

                    self.inputDeleteList[x].blockSignals(True)
                    self.inputDeleteList[x].setChecked(False)
                    self.inputDeleteList[x].blockSignals(False)
            procs.guiProcess = False
        self.toggleAllCheckBox.blockSignals(False)
        self.deleteAllCheckBox.blockSignals(False)

    def makeUI(self):
        self.viewerMenuWidget = viewerMenu(viewerList)
        return self.viewerMenuWidget
