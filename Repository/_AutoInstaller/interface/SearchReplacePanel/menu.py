
#search and replace panel
import SearchReplacePanel
def addSRPanel():
    '''Run the panel script and add it as a tab into the pane it is called from'''
    myPanel = SearchReplacePanel.SearchReplacePanel()
    return myPanel.addToPane()
# THIS LINE WILL ADD THE NEW ENTRY TO THE PANE MENU
nuke.menu('Pane').addCommand('SearchReplace', addSRPanel)
# THIS LINE WILL REGISTER THE PANEL SO IT CAN BE RESTORED WITH LAYOUTS
nukescripts.registerPanel('com.ohufx.SearchReplace', addSRPanel)