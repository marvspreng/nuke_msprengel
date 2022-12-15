nuke.pluginAddPath("./viewerLock")

import viewerLock
import nukescripts

class viewerLockPanel(nukescripts.PythonPanel):
    def __init__(self):
        super(viewerLockPanel, self).__init__("Viewer Lock", "viewerLock.id")
        self.viewerLockKnob = nuke.PyCustom_Knob( "viewerLock_pyknob", "", "viewerLock.viewerMenu(viewerLock.viewerList)" )
        self.addKnob( self.viewerLockKnob )

def addVLPanel(openOn=None):
    if not "vLPanel" in locals() and not "vLPanel" in globals(): # okay this is pretty disgusting, I need to rewrite this whole section
        global vLPanel
        vLPanel = viewerLockPanel()
    try:
        return vLPanel.addToPane(nuke.getPaneFor("viewerLock.id")) # reopen panel where it already is. don"t know how to simply focus on the panel if it exists.
    except:
        return vLPanel.addToPane(openOn)

def viewerMenuCallback():
    if "vLPanel" in globals():
        vLPanel.viewerLockKnob.getObject().viewerMenuWidget.updateUI()

nuke.addKnobChanged(viewerMenuCallback, nodeClass="Viewer")
nuke.addOnDestroy(viewerMenuCallback)
nuke.addUpdateUI(viewerMenuCallback)
nuke.menu("Pane").addCommand("Viewer Lock", addVLPanel)
nukescripts.registerPanel("viewerLock.id", addVLPanel)

m = nuke.menu("Nuke").addMenu("Viewer Lock")
vLC = m.addMenu("Connect")
vLL = m.addMenu("Lock")
vLU = m.addMenu("Unlock")

vLC.addCommand("Connect Input 1", "viewerLock.connect(0)", '1', shortcutContext=2)
vLC.addCommand("Connect Input 2", "viewerLock.connect(1)", '2', shortcutContext=2)
vLC.addCommand("Connect Input 3", "viewerLock.connect(2)", '3', shortcutContext=2)
vLC.addCommand("Connect Input 4", "viewerLock.connect(3)", '4', shortcutContext=2)
vLC.addCommand("Connect Input 5", "viewerLock.connect(4)", '5', shortcutContext=2)
vLC.addCommand("Connect Input 6", "viewerLock.connect(5)", '6', shortcutContext=2)
vLC.addCommand("Connect Input 7", "viewerLock.connect(6)", '7', shortcutContext=2)
vLC.addCommand("Connect Input 8", "viewerLock.connect(7)", '8', shortcutContext=2)
vLC.addCommand("Connect Input 9", "viewerLock.connect(8)", '9', shortcutContext=2)
vLC.addCommand("Connect Input 0", "viewerLock.connect(9)", '0', shortcutContext=2)
vLL.addCommand("Lock Input 1", "viewerLock.lock(0)", "ctrl+alt+1")
vLL.addCommand("Lock Input 2", "viewerLock.lock(1)", "ctrl+alt+2")
vLL.addCommand("Lock Input 3", "viewerLock.lock(2)", "ctrl+alt+3")
vLL.addCommand("Lock Input 4", "viewerLock.lock(3)", "ctrl+alt+4")
vLL.addCommand("Lock Input 5", "viewerLock.lock(4)", "ctrl+alt+5")
vLL.addCommand("Lock Input 6", "viewerLock.lock(5)", "ctrl+alt+6")
vLL.addCommand("Lock Input 7", "viewerLock.lock(6)", "ctrl+alt+7")
vLL.addCommand("Lock Input 8", "viewerLock.lock(7)", "ctrl+alt+8")
vLL.addCommand("Lock Input 9", "viewerLock.lock(8)", "ctrl+alt+9")
vLL.addCommand("Lock Input 0", "viewerLock.lock(9)", "ctrl+alt+0")

vLL.addSeparator()

vLL.addCommand("Lock All", "viewerLock.lockAll()", "ctrl+alt+v")
vLU.addCommand("Unlock Input 1", "viewerLock.unlock(0)", "ctrl+shift+1")
vLU.addCommand("Unlock Input 2", "viewerLock.unlock(1)", "ctrl+shift+2")
vLU.addCommand("Unlock Input 3", "viewerLock.unlock(2)", "ctrl+shift+3")
vLU.addCommand("Unlock Input 4", "viewerLock.unlock(3)", "ctrl+shift+4")
vLU.addCommand("Unlock Input 5", "viewerLock.unlock(4)", "ctrl+shift+5")
vLU.addCommand("Unlock Input 6", "viewerLock.unlock(5)", "ctrl+shift+6")
vLU.addCommand("Unlock Input 7", "viewerLock.unlock(6)", "ctrl+shift+7")
vLU.addCommand("Unlock Input 8", "viewerLock.unlock(7)", "ctrl+shift+8")
vLU.addCommand("Unlock Input 9", "viewerLock.unlock(8)", "ctrl+shift+9")
vLU.addCommand("Unlock Input 0", "viewerLock.unlock(9)", "ctrl+shift+0")

vLU.addSeparator()

vLU.addCommand("Unlock All", "viewerLock.unlockAll()", "ctrl+shift+v")

m.addSeparator()

m.addCommand("Viewer Menu", "addVLPanel(nuke.getPaneFor(\"Properties.1\"))", "shift+v")