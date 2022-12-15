#Copyright (c) 2016-2021, Wouter Gilsing
#All rights reserved.

import os
import nuke

#----------------------------------------------------------------------------------------------------------
# Preferences
#----------------------------------------------------------------------------------------------------------

class Preferences:
    
    preferencesNode = nuke.toNode('preferences')

    def addToPreferences(self,knobObject, tooltip = None):
        '''
        Add a knob to the preference panel.
        Save current preferences to the prefencesfile in the .nuke folder.
        '''

        if knobObject.name() not in self.preferencesNode.knobs().keys():

            if tooltip != None:
                knobObject.setTooltip(tooltip)

            self.preferencesNode.addKnob(knobObject)
            self.savePreferencesToFile()
            return self.preferencesNode.knob(knobObject.name())

    def savePreferencesToFile(self):
        '''
        Save current preferences to the prefencesfile in the .nuke folder.
        Pythonic alternative to the 'ok' button of the preferences panel.
        '''

        nukeFolder = os.path.expanduser('~') + '/.nuke/'
        preferencesFile = nukeFolder + 'preferences{}.{}.nk'.format(nuke.NUKE_VERSION_MAJOR, nuke.NUKE_VERSION_MINOR)

        preferencesNode = nuke.toNode('preferences')

        customPrefences = preferencesNode.writeKnobs( nuke.WRITE_USER_KNOB_DEFS | nuke.WRITE_NON_DEFAULT_ONLY | nuke.TO_SCRIPT | nuke.TO_VALUE )
        customPrefences = customPrefences.replace('\n','\n  ')

        preferencesCode = 'Preferences {\n inputs 0\n name Preferences%s\n}' %customPrefences

        # write to file
        openPreferencesFile = open( preferencesFile , 'w' )
        openPreferencesFile.write( preferencesCode )
        openPreferencesFile.close()


    def updatePreferences(self):
        
        preferencesNode = nuke.toNode('preferences')
        firstLaunch = True
        location = preferencesNode.knob('nodeboardShareLocation').value()
        share = preferencesNode.knob('nodeboardShareShortcut').value()
        get = preferencesNode.knob('nodeboardGetShortcut').value()
        cat = preferencesNode.knob('nodeboardDefaultCategory').value()
        
        for i in preferencesNode.knobs().keys():
            if 'nodeboard' in i:
                preferencesNode.removeKnob(preferencesNode.knob(i))
                firstLaunch = False

        #remove TabKnob
        try:
            preferencesNode.removeKnob(preferencesNode.knob('nodeboardLabel'))
        except:
            pass

        if not firstLaunch:
            self.savePreferencesToFile()

        self.addPreferences()
        preferencesNode.knob('nodeboardShareLocation').setValue(location)
        preferencesNode.knob('nodeboardShareShortcut').setValue(share)
        preferencesNode.knob('nodeboardGetShortcut').setValue(get)
        if cat != None:
            preferencesNode.knob('nodeboardDefaultCategory').setValue(cat)


        self.savePreferencesToFile()

    def addPreferences(self):
        '''
        Add knobs to the preferences needed for this module to work properly.
        '''
        
        self.addToPreferences(nuke.Tab_Knob('nodeboardLabel','NodeBoard'))
        self.addToPreferences(nuke.Text_Knob('nodeboardGeneralLabel','<b>General</b>'))
        self.addToPreferences(nuke.File_Knob('nodeboardShareLocation','Share location'))
        shareknob = nuke.String_Knob('nodeboardShareShortcut','Share Shortcut')
        shareknob.setValue('Ctrl+Alt+C')
        self.addToPreferences(shareknob)
        getknob = nuke.String_Knob('nodeboardGetShortcut','Get Shortcut')
        getknob.setValue('Ctrl+Alt+V')
        self.addToPreferences(getknob)
        knob = nuke.PyScript_Knob('nodeboardresetshortcut','set', 'sharetoolfromdag.resetShortcuts()')
        knob.clearFlag(nuke.STARTLINE)
        tooltip = "Apply new shortcut."
        self.addToPreferences(knob, tooltip)




        currentDir = os.path.dirname(os.path.realpath(__file__))    
        folderList = next(os.walk(currentDir))[1]
        catList = list()
        if len(folderList) > 0:
            for item in folderList:
                if item != '__pycache__' and item != 'icons':
                    catList.append(item)
        if len(catList) == 0:
            catList.append('Default')
        defaultCat = nuke.Enumeration_Knob('nodeboardDefaultCategory', 'Default Category', catList)
        self.addToPreferences(defaultCat)
        

        dummyTab = nuke.Tab_Knob('nodeboardDummyTab', 'Dummy')
        dummyTab.setFlag(0x00040000)

        self.addToPreferences(dummyTab)
        
        
        
        self.savePreferencesToFile()
