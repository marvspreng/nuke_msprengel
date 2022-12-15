import nuke
import nukescripts
import zipfile
import json
import shutil
import os
import re
from PySide2.QtWidgets import QComboBox, QLineEdit, QWidget
from QCustomWidgets import QLabelButton, Collapse
from preferences import Preferences
try:
    from PySide import QtWidgets, QtCore
except ImportError:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from PySide2 import QtGui
    from PySide2 import QtOpenGL


#main nuke dockable window
class CreateNodeBoard(QtWidgets.QWidget):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)

        #ADD PREFERENCES MENU TO NUKE
        self.preferences = Preferences()
        self.preferences.addPreferences()
        self.shareLocation = self.preferences.preferencesNode.knob('nodeboardShareLocation').value()
        self.defaultCategory = self.updateDefaultCategory()

        #modifyscript toggle
        self.modifyToggle = False
        self.nukePathSeparator = "/"

        self.currentDir = os.path.dirname(os.path.realpath(__file__))
        self.currentCat = os.path.sep  + self.updateCurrentCategory() + os.path.sep

        self.toolPath = self.getFullPathWithExt()

    ################################################################################
    # GUI
    ################################################################################
  
        self.setMinimumWidth(350)        
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.mainLayout)
        self.target = None
        self.targetWidget = None
        self.setAcceptDrops(True)

    ################################################################################
    # GUI - MAIN MENU
    ################################################################################

        self.mainMenuWidget = QtWidgets.QWidget()
        self.mainMenuWidget.setAcceptDrops(True)

        ################################################################################
        #CATEGORIES
        ################################################################################

        self.comboBoxWidget = QtWidgets.QWidget()
        self.comboBoxLayout = QtWidgets.QHBoxLayout(self.comboBoxWidget)

        #COMBO BOX
        self.comboBox = QtWidgets.QComboBox(self.mainMenuWidget)
        self.comboBox.setEditable(True)
        self.loadCategories()
        self.setDefaultItem()
        self.comboBox.currentIndexChanged.connect(self.switchCat)
        self.comboBox.setMinimumSize(150,20)
        self.comboBox.setInsertPolicy(QComboBox.NoInsert)
        self.comboBox.setToolTip('Current category context. Click the drop down arrow to choose a different category.')

        #CREATE NEW CAT BUTTON
        self.classesListAddButton = QLabelButton('add',self.comboBoxWidget)
        self.classesListAddButton.clicked.connect(self.createNewCat)
        self.classesListAddButton.setToolTip('Adds a new category.')
        
        #REMOVE CAT BUTTON
        self.classesListRemoveButton = QLabelButton('remove',self.comboBoxWidget)
        self.classesListRemoveButton.clicked.connect(self.deleteCategory)
        self.classesListRemoveButton.setToolTip('Deletes the current category.')

        #RENAME CAT BUTTON
        self.classesListRenameButton = QLabelButton('rename',self.comboBoxWidget)
        self.classesListRenameButton.clicked.connect(self.renameCategory)
        self.classesListRenameButton.setToolTip('Renames the current category.')

        #SHARE CAT BUTTON
        self.classesListShareButton = QLabelButton('moveUp',self.comboBoxWidget)
        self.classesListShareButton.clicked.connect(self.shareCategory)
        self.classesListShareButton.setToolTip('Shares the current category to the specified location in Prefereences - NodeBoard.')        

        #GET CAT BUTTON
        self.classesListGetButton = QLabelButton('moveDown',self.comboBoxWidget)
        self.classesListGetButton.clicked.connect(self.getCategory)
        self.classesListGetButton.setToolTip('Downloads a category from the specified location in Prefereences - NodeBoard.')

        #SYNC TO W_HOTBOX CAT BUTTON
        self.classesListSyncToHotboxbutton = QLabelButton('synctohotbox',self.comboBoxWidget)
        self.classesListSyncToHotboxbutton.clicked.connect(lambda: self.syncToHotbox('cat'))
        self.classesListSyncToHotboxbutton.setToolTip('Syncs the current category into W_hotbox - All. Important notice: Further modification of the category inside the NodeBoard does not sync the changes to W_hotbox. It needs to be done from the W_hotbox manager')

        #EXPORT CAT BUTTON
        self.classesListExportbutton = QLabelButton("Export", self.comboBoxWidget)
        self.classesListExportbutton.clicked.connect(self.exportZip)
        self.classesListExportbutton.setToolTip('Exports the current category as a ZIP.')

        #IMPORT CAT BUTTON
        self.classesListImportbutton =QLabelButton("Import", self.comboBoxWidget)
        self.classesListImportbutton.clicked.connect(self.importZip)
        self.classesListImportbutton.setToolTip('Imports a category from selected location into the NodeBoard.')

        #CREATE BUTTON
        self.createButton = QtWidgets.QPushButton("Add ToolSet", self.comboBoxWidget)
        self.createButton.clicked.connect(self.saveNewSrcipt)
        self.createButton.setToolTip('Creates a new toolset entry in the current category from the selected nodes.')

        #ADD ALL WIDGETS TO THE LAYOUT
        self.comboBoxLayout.addWidget(self.comboBox)
        self.comboBoxLayout.addWidget(self.classesListAddButton)
        self.comboBoxLayout.addWidget(self.classesListRemoveButton)
        self.comboBoxLayout.addWidget(self.classesListRenameButton)
        self.comboBoxLayout.addWidget(self.classesListShareButton)
        self.comboBoxLayout.addWidget(self.classesListGetButton)   
        self.comboBoxLayout.addWidget(self.classesListSyncToHotboxbutton)
        self.comboBoxLayout.addStretch(1)
        self.comboBoxLayout.addWidget(self.createButton)
        #self.comboBoxLayout.addWidget(self.classesListExportbutton)
        #self.comboBoxLayout.addWidget(self.classesListImportbutton)

        ###################################################################################
        #TOOLS
        ###################################################################################
        
        self.mainMenuButtonWidget = QtWidgets.QWidget(self.mainMenuWidget)
        self.mainMenuButtonWidget.setGeometry(QtCore.QRect(0, 0, 251, 41))
                
        self.mainMenuButtonLayout = QtWidgets.QVBoxLayout(self.mainMenuButtonWidget)
        self.mainMenuButtonLayout.setContentsMargins(0, 0, 0, 0)
        
        #MODIFY BUTTON
        self.modifyButton = QLabelButton('modify',self.mainMenuButtonWidget)
        self.modifyButton.clicked.connect(self.modifyScript)
        self.modifyButton.setToolTip('Creates a backdrop in your DAG at the cursor position to allow the modification of selected toolset.')
        
        #DELETE BUTTOn
        self.deleteButton = QLabelButton('remove',self.mainMenuButtonWidget)
        self.deleteButton.clicked.connect(self.deleteScript)
        self.deleteButton.setToolTip('Deletes the currently selected toolset.')

        #RENAME BUTTOn
        self.renameButton = QLabelButton('rename',self.mainMenuButtonWidget)
        self.renameButton.clicked.connect(self.renameScript)
        self.renameButton.setToolTip('Renames the currently selected toolset')

        #SHARE Button
        self.shareButton = QLabelButton('moveUp',self.mainMenuButtonWidget)
        self.shareButton.clicked.connect(self.shareScript)
        self.shareButton.setToolTip(('Share the currently selected toolset to the server specified directory'))

        #GET Button
        self.getButton = QLabelButton('moveDown',self.mainMenuButtonWidget)
        self.getButton.clicked.connect(self.getScript)
        self.getButton.setToolTip(('Moves a toolset fromn the server specified directory into the current category'))

        #SYNC TO W_HOTBOX Button
        self.syncWButton = QLabelButton('synctohotbox',self.mainMenuButtonWidget)
        self.syncWButton.clicked.connect(self.syncToHotbox)
        self.syncWButton.setToolTip('Syncs the selected ToolSet into the W_hotbox if installed.')
        
        self.mainMenuButtonLayout.addWidget(self.deleteButton)
        self.mainMenuButtonLayout.addWidget(self.renameButton)
        self.mainMenuButtonLayout.addWidget(self.modifyButton)
        self.mainMenuButtonLayout.addWidget(self.shareButton)
        self.mainMenuButtonLayout.addWidget(self.getButton)
        self.mainMenuButtonLayout.addWidget(self.syncWButton)
        self.mainMenuButtonLayout.addStretch(1)

        #search bar
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText('Search tool...')
        self.searchbar.textChanged.connect(self.searchScript)
        self.searchbar.returnPressed.connect(self.loadScriptfromList)
        self.searchbar.editingFinished.connect(self.finishsearch)
        
        self.toolWidget = QtWidgets.QWidget(self.mainMenuWidget)
        self.toolLayout = QtWidgets.QHBoxLayout(self.toolWidget)

        #TOOL LIST
        self.listWidget = QtWidgets.QListWidget(self.mainMenuWidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 40, 241, 191))
        self.listWidget.itemActivated.connect(self.loadScriptfromList)
        self.listWidget.installEventFilter(self)
        self.toolLayout.addWidget(self.listWidget)
        self.toolLayout.addWidget(self.mainMenuButtonWidget)

        #COLOR LABEL
        self.colorLabel = QtWidgets.QLabel("NODEBOARD - click to add a coloured button")
       
        ###################################################################################
        #COLOR PICK LAYOUT      
        ###################################################################################

        self.buttonWidget = QtWidgets.QWidget(self.mainMenuWidget)
        self.menubuttonsLayout = QtWidgets.QHBoxLayout(self.buttonWidget)
        colorpickLayout = QtWidgets.QVBoxLayout()

        # COLOR  PICK BUTTON LAYOUT ROW 1
        self.colourWidget1 = QtWidgets.QWidget()
        self.colorButtonmainMenuLayout1 = QtWidgets.QHBoxLayout(self.colourWidget1)
        colorpickLayout.addWidget(self.colourWidget1)
        self.colorButtonmainMenuLayout1.setContentsMargins(0, 0, 0, 0)

        # COLOR PICK BUTTON LAYOUT ROW 2
        self.colorWidget2 = QtWidgets.QWidget()
        self.colorButtonmainMenuLayout2 = QtWidgets.QHBoxLayout(self.colorWidget2)
        colorpickLayout.addWidget(self.colorWidget2)
        self.colorButtonmainMenuLayout2.setContentsMargins(0, 0, 0, 0)

        #Load color picking buttons from JSON
        self.loadColourPickButtons()
        #Load ToolSets from /NodeBoard folder in /.nuke
        self.loadTools()

        self.colorButtonmainMenuLayout1.addStretch(1)  
        self.colorButtonmainMenuLayout2.addStretch(1) 

        #create delete all button    
        self.deleteAllButton = QtWidgets.QPushButton('Delete All', self.buttonWidget)
        self.deleteAllButton.clicked.connect(self.deleteNBButtons)
        self.deleteAllButton.setFixedSize(100,22)
        self.deleteAllButton.setToolTip('Deletes all buttons from nodebaord.')

        self.menubuttonsLayout.addLayout(colorpickLayout)
        self.menubuttonsLayout.addWidget(self.deleteAllButton)   
        
        ###################################################################################
 
        self.mainMenuLayout = Collapse(title= "ToolSets")
        self.mainMenuLayout.addWidget(self.searchbar)
        self.mainMenuLayout.addWidget(self.toolWidget)
        self.mainMenuLayout.addWidget(self.colorLabel)
        self.mainMenuLayout.addWidget(self.buttonWidget)
        self.mainMenuLayout.setMaximumHeight(400)
       
        self.mainLayout.addWidget(self.comboBoxWidget)
        self.mainLayout.addWidget(self.mainMenuLayout)

    ################################################################################
    # GUI - NODE BOARD
    ################################################################################
      
        self.nodeBoardWidget = QtWidgets.QWidget()
        self.nodeBoardWidget.setAcceptDrops(True)
        nodeBoardVLayout = QtWidgets.QVBoxLayout()
        self.nodeBoardWidget.setLayout(nodeBoardVLayout)

        self.nodeBoardMenuLayout = QtWidgets.QHBoxLayout()
        self.nodeBoardMenuLayout.setAlignment(QtCore.Qt.AlignCenter)
        nodeBoardVLayout.addLayout(self.nodeBoardMenuLayout)

        #create a grid layout inside nodeBoaardVLayout and load buttons from JSON
        self.userButtonLayout = QtWidgets.QGridLayout()
        nodeBoardVLayout.addLayout(self.userButtonLayout)
        self.loadNBButtonsJSON()
        self.userButtonLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.mainLayout.addWidget(self.nodeBoardWidget)
        nodeBoardVLayout.addStretch(1)
    
    ################################################################################
    # CREATE PATH
    ################################################################################

    #creates a dictionary with the path and the extension of current toolset
    def getFullPathWithExt(self):        
        if self.defaultCategory not in os.listdir(self.currentDir):
            try:
                os.mkdir(self.currentDir + self.currentCat)
                with open(self.currentDir +self.currentCat  + 'buttons.json', 'w'):
                    data = {'userButtons': []}
                    self.writeJson(data)
            except Exception as e: 
                nuke.message("ERROR - run as admin")
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    (e)
                return None
        if nuke.env['nc']:
            nukeExt = ".nknc"
        #elif nuke.env['indie']:
            #nukeExt = ".nkind"
        else:
            nukeExt = ".nk"
        fullPath = self.currentDir + self.currentCat
        return {"path": fullPath, "ext": nukeExt}

    ################################################################################
    # NB FUNCTIONS
    ################################################################################
    def updateCurrentCategory(self):
        print('')
        try:
            return self.comboBox.currentText()
        except:
            return self.defaultCategory

    def exportZip(self):
        path = nuke.getFilename("get Directory")
        subfolders = [ f.path for f in os.scandir(self.currentDir) if f.is_dir() and os.path.basename(f.path) != "__pycache__" ]
        print(subfolders)
        with zipfile.ZipFile(path + self.nukePathSeparator +  "zip_name.zip", 'w') as z:
            for folder in subfolders:
                self.zip_compression_tree(folder,z)

    def zip_compression_tree(self, root_path,z):
        lenDirPath = len(root_path)
        for root, dirs, files in os.walk(root_path):

            for file in files:
                filePath = os.path.join(root, file)
                z.write(filePath , filePath[lenDirPath-len(os.path.basename(root)) :] )
    
    def importZip(self):
         path = nuke.getFilename("get zip file")
         with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(self.currentDir)

    #filter for context menu in self.listWidget
    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.ContextMenu and source is self.listWidget):

            menu = QtWidgets.QMenu()
            delete = QtWidgets.QAction("Delete")
            rename = QtWidgets.QAction("Rename")
            modify = QtWidgets.QAction("Modify")
            share = QtWidgets.QAction("Share")
            get = QtWidgets.QAction("Get")
            sendHbox = QtWidgets.QAction("Sync to W_hotbox")
            
            menu.addAction(delete)
            menu.addAction(rename)
            menu.addAction(modify)
            menu.addAction(share)
            menu.addAction(get)
            menu.addAction(sendHbox)
            
            menu_click = menu.exec_(event.globalPos())
            
            try:
                item = source.itemAt(event.pos())
            except Exception as e:
                print("No item selected")

            if menu_click == delete :
                self.deleteScript()
            if menu_click == rename :
                self.renameScript()
            if menu_click == modify :
                self.modifyScript()
            if menu_click == share :
                self.shareScript()
            if menu_click == get :
                self.getScript()
            if menu_click == sendHbox :
                self.syncToHotbox('tool')
            return True

        return super(CreateNodeBoard, self).eventFilter(source, event)

    #paste script into DAG after pressing a button
    def loadScriptfromButton(self):
        itemName = self.sender().text()
        fullPath = self.getFullPathWithExt()
        if fullPath != None: 
            nuke.nodePaste(fullPath["path"] + itemName + fullPath["ext"])

    #assign custom color and create a button in NB      
    def createButtonfromCustomColor(self):
        nodeName = self.getItemName('tool')
        #convert to RGB
        nodeColorInt = nuke.getColor()
        nodeColorRGB = [nodeColorInt >> shift & 255 for shift in range(24,0,-8)]
        nodeColorRepaired = []
        for color in nodeColorRGB:
            value = re.sub('[^0-9]','', str(color))
            nodeColorRepaired.append(int(value))           
        background = "background-color: rgb" + str(tuple(nodeColorRepaired))
        self.createNBButton(nodeName, background)
    
    #assign color and create a button in NB 
    def createButtonFromColor(self):
        nodeName = self.getItemName('tool')
        background = self.sender().styleSheet()
        self.createNBButton(nodeName, background)

    #delete all buttons from NB
    def deleteNBButtons(self):
        if nuke.ask("Do you really want to delete all buttons from NodeBoard?"):
            self.deleteButtonsFromUserButtonLayout()
            
    def deleteButtonsFromUserButtonLayout(self):
        while self.userButtonLayout.count():
                child = self.userButtonLayout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
        self.removeButtonsFromJson()
   
    def createNBButton(self,nodeName, background):
        #create new button set BG color and connect signal
        button = self.setNBButton(nodeName, background)
        
        #check whether the button already exists
        data = self.openJson()
        userButtons = data['userButtons']
        nameCheck = []
        for b in userButtons:            
            nameCheck.append(b['title'])
        buttonLimit = nameCheck.count(nodeName)

        #add button to NB                
        if buttonLimit < 1 or len(userButtons) == 0:
            userButtons = {"color": background, "title": nodeName}
            self.appendButtonsToJson(userButtons)            
            self.addNBButton(button)
        else:
            nuke.message("This button is already created.")
   
    # set parameters of NB button   
    def setNBButton(self, nodeName, background):
        button = QtWidgets.QPushButton(str(nodeName), self.nodeBoardWidget)
        if len(nodeName) > 9:
            button.setStyleSheet(background + "; text-align:left"  + "; color: white"  + "; font-size: 14px")
        else:
            button.setStyleSheet(background+  "; color: white" + "; font-size: 14px")
        button.setMaximumSize(80,80)
        button.clicked.connect(self.loadScriptfromButton)
        button.setToolTip('Left click to paste to DAG, Middle click to swap around, Right click to open context menu.')
        return button

    def addNBButton(self,button):
        #Add button menu
        button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        button.customContextMenuRequested.connect(self.createButtonMenu)
       
        #add button to userButtonLayout grid
        i = self.userButtonLayout.count()
        self.userButtonLayout.addWidget(button, i // 6, i % 6)

    #creates a 'Delete' pop up menu on each button in NB
    def createButtonMenu(self, eventPosition):
        child = self.childAt(self.sender().mapTo(self, eventPosition))
        self.popMenu = QtWidgets.QMenu(self)
        delete = self.popMenu.addAction('Delete')
        action = self.popMenu.exec_(child.mapToGlobal(eventPosition))

        if action == delete:
            buttonName = child.text()
            self.removeButtonFromJson(buttonName)           
            self.userButtonLayout.removeWidget(child)
            child.deleteLater()
            child = None
            self.renderButtons(0)
    
    #loads button information from JSOn
    def loadNBButtonsJSON(self):
        data = self.openJson()
        for button in data['userButtons']:
            nodeName = button['title']
            background = button['color']
            self.loadNBBUttons(nodeName, background)

    #loads buttons to NB
    def loadNBBUttons(self, nodeName, background):
        button = self.setNBButton(nodeName, background)
        self.addNBButton(button)

    def openJson(self):
        with open(self.currentDir + self.currentCat + 'buttons.json') as f:
            data = json.load(f)
        return data
    
    def writeJson(self, data):
        with open(self.currentDir +  self.currentCat +'buttons.json', 'w') as f:
            json.dump(data, f, indent = 4)
    
    def appendButtonsToJson(self, userButtons):
        data = self.openJson()
        temp = data["userButtons"]
        temp.append(userButtons)
        self.writeJson(data)

    def removeButtonsFromJson(self):        
            data = self.openJson()
            temp = data["userButtons"]
            del temp [:]
            self.writeJson(data)
    
    #deletes all buttons and loads them back from JSON based on the the buttons order in NB
    def renderButtons(self, token):
        data = self.openJson()
        temp = data["userButtons"]
        del temp [:]
 
        for i in range(self.userButtonLayout.count()):
            if token == 0:
                nodeName = self.userButtonLayout.itemAt(i).widget().text()
                background = self.userButtonLayout.itemAt(i).widget().styleSheet()
            else:
                nodeName = self.userButtonLayout.itemAtPosition(i // 6, i % 6).widget().text()
                background = self.userButtonLayout.itemAtPosition(i // 6, i % 6).widget().styleSheet()

            userButtons = {"color": background, "title": nodeName}
            temp.append(userButtons)
        self.writeJson(data)

        while self.userButtonLayout.count():
            child = self.userButtonLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.loadNBButtonsJSON()
   
    #deletes a button from JSON
    def removeButtonFromJson(self, button):
        data = self.openJson()
        temp = data["userButtons"]
        for b in temp:
            if b["title"] == button:
                temp.remove(b)
        self.writeJson(data)

    ################################################################################
    # MAIN MENU FUNCTIONS
    ################################################################################
    
    # SEARCH BAR FUNCTIONS
    ################################################################################

    #use up and down keys inside the searchbar to navigate inside the self.listWidget
    #define key press
    def keyPressEvent(self, e):
        if e.key()  == 0x01000013 :
            self.navigatesearch('up')
        elif e.key() == 0x01000015 :   
            self.navigatesearch('down')
    
    #this function is a mess but it does the job
    def navigatesearch(self,token):
        if token == 'up':
            row = self.listWidget.currentRow()
            if row != 0:
                self.listWidget.setCurrentRow(row-1)
            else:
                self.listWidget.setCurrentRow(0)
        else:
            row = self.listWidget.currentRow()
            if row >= 0 and row < (self.listWidget.count()-1):
                if self.listWidget.item(row+1).isHidden():
                    try:
                        while self.listWidget.item(row+1).isHidden():
                            self.listWidget.setCurrentRow(row+1)
                            row = row + 1
                        row = self.listWidget.currentRow()
                        if self.listWidget.item(row).isHidden():
                            self.listWidget.setCurrentRow(row+1)
                    except:
                        self.listWidget.setCurrentRow(0)
                        row = self.listWidget.currentRow()
                        while self.listWidget.item(row).isHidden():
                            self.listWidget.setCurrentRow(row+1)
                            row = row + 1

                else:
                    self.listWidget.setCurrentRow(row+1)

            else:
                self.listWidget.setCurrentRow(0)
                row = self.listWidget.currentRow()
                while self.listWidget.item(row).isHidden():
                    self.listWidget.setCurrentRow(row+1)
                    row = row + 1
    
    #display only ToolSets that are matching the text, hide  others
    def searchScript(self,text):
        if self.searchbar.displayText():
            switch = False
            for i in range(self.listWidget.count()):
                entry = self.listWidget.item(i)
                if text.lower() not in entry.text().lower():
                    entry.setHidden(True)
                  
                else:
                    entry.setHidden(False)
                    if switch == False:
                        entry.setSelected(True)
                        self.listWidget.setCurrentRow(i)
                        switch = True
        else:
            self.finishsearch()
    
    #unhide all ToolSets and reset
    def finishsearch(self):
        self.searchbar.clear()
        for i in range(self.listWidget.count()):
                entry = self.listWidget.item(i)
                entry.setHidden(False)
    
    ################################################################################

    def renameScript(self):
        newItemName = nuke.getInput('Enter new name:')
    
        if self.listWidget.findItems(newItemName, QtCore.Qt.MatchRecursive):
            nuke.message("Specified name already exists")
        else:
            itemName = self.getItemName('tool')
            path = self.getFullPathWithExt()
            fullPath = path["path"] + itemName + path["ext"]
            newFullPath = path["path"] + newItemName + path["ext"]
            #change to .nk file
            try:
                os.rename(fullPath, newFullPath)
            except:
                nuke.message("Error! try relaunching Nuke.")
            #change the list entry name
            selectedItem = self.listWidget.selectedItems()[0]
            selectedItem.setText(newItemName)
            #change button name in nodeboard
            for i in range(self.userButtonLayout.count()):
                button = self.userButtonLayout.itemAt(i).widget()
                if button.text() == itemName:
                    button.setText(newItemName)
                    background = button.styleSheet()
                    if len(newItemName) <= 9:
                        button.setStyleSheet(background + "; text-align:middle")
                    else:
                        button.setStyleSheet(background + "; text-align:left")

        #change the button entry in buttons.json
        data = self.openJson()
        temp = data["userButtons"]
        for b in temp:
            if b["title"] == itemName:
                b['title'] = newItemName
        self.writeJson(data)  

    def deleteScript(self):
        #delete from OS
        if nuke.ask('Are you sure you want to delete this?'):      
            itemName = self.getItemName('tool')
            path = self.getFullPathWithExt()
            fullPath = path["path"] + itemName + path["ext"]
            os.remove(fullPath)
            rowNumber = self.listWidget.currentRow()
            self.listWidget.takeItem(rowNumber)

            #delete from JSON
            self.removeButtonFromJson(itemName)
            #delete from NB
            for i in range(self.userButtonLayout.count()):
                child = self.userButtonLayout.itemAt(i).widget()
                if child.text() == itemName:
                    self.userButtonLayout.removeWidget(child)
                    child.deleteLater()
                    child = None
            self.renderButtons(0)
    
    #copy the ToolSet into the server location specified in the preferences
    def shareScript(self):
        self.shareLocation = self.preferences.preferencesNode.knob('nodeboardShareLocation').value()
        try: 
            selection = self.getItemName('tool')                 
            pathExt = self.getFullPathWithExt()
            fullPath = pathExt['path'] + selection + pathExt['ext']
            if self.shareLocation != '':
                self.emptyShareLocation(self.shareLocation)
                shutil.copy(fullPath, self.shareLocation)
            else:
                nuke.message("Please specify the share location in the preferences first!")
                
        except IndexError:
            nuke.message('Please select a tool to share.')
    
    #delete all files from the share location 
    def emptyShareLocation(self, location):
        for root, dirs, files in os.walk(location):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.remove(os.path.join(root, dir))
    
    #copy and paste the ToolSet from share location into the DAG
    def getScript(self):
        for root,dirs,files in os.walk(self.shareLocation):
            for file in files:
                if file not in os.listdir(self.currentDir + self.currentCat):
                    shutil.copy(os.path.join(root, file), self.currentDir + self.currentCat)
                    self.loadTools()
                    self.emptyShareLocation(self.shareLocation)
                else:
                    nuke.message('the tool already exists in your category')
    
    #create a backdrop modification area where you can modify the current Toolset and save it
    def modifyScript(self):
        itemName = self.getItemName('tool')        
        fullPath = self.getFullPathWithExt()
        #load Script into a BD and start modification inside DAG
        if self.modifyToggle == False:
            nuke.nodePaste(fullPath["path"] + itemName + fullPath["ext"])
            self.autoBackdrop()
            self.modifyButton.setStyleSheet('background-color: orange')
            self.modifyButton.setToolTip('Click to save.')
            self.modifyToggle = True
            self.listWidget.clear()
            self.addToolToList(itemName, 'tool')
            self.listWidget.item(0).setSelected(True)
            nuke.addOnCreate(self.nodeInBD)
 
        else:   
            backdrop = nuke.toNode("Modify")
            backdrop.selectNodes(True)
            backdropNodes = nuke.selectedNodes()
            nuke.nodeCopy(fullPath["path"] + itemName + fullPath["ext"])
            for node in backdropNodes:
                nuke.delete(node)
            backdrop = nuke.toNode("Modify")
            nuke.delete(backdrop)
            self.modifyButton.setStyleSheet('background-color: ')
            self.modifyButton.setToolTip('Creates a backdrop in your DAG at the cursor position to allow the modification of selected toolset.')
            self.modifyToggle = False
            self.listWidget.clear()
            self.loadTools()
            nuke.removeOnCreate(self.nodeInBD)

            selectedNodes = nuke.selectAll()
            nuke.zoomToFitSelected()    

    #create a custom BD for modification purposes
    def autoBackdrop(self):
        selNodes = nuke.selectedNodes() 
        if not selNodes: 
            return nuke.nodes.BackdropNode() 

        for node in selNodes:
            x = node['xpos'].value()
            y = node['ypos'].value()
            node['xpos'].setValue(x +1000000)
            node['ypos'].setValue(y +1000000)

        # Calculate bounds for the backdrop node. 
        bdX = min([node.xpos() for node in selNodes]) 
        bdY = min([node.ypos() for node in selNodes]) 
        bdW = max([node.xpos() + node.screenWidth() for node in selNodes]) - bdX 
        bdH = max([node.ypos() + node.screenHeight() for node in selNodes]) - bdY 
        
        zOrder = -10
                
        # Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively 
        left, top, right, bottom = (-10, -80, 500, 150) 
        bdX += left 
        bdY += top 
        bdW += (right - left) 
        bdH += (bottom - top) 
        
        n = nuke.nodes.BackdropNode(xpos = bdX, 
                                    bdwidth = bdW, 
                                    ypos = bdY, 
                                    bdheight = bdH, 
                                    tile_color = 4290707711, 
                                    note_font_size=42, 
                                    z_order = zOrder ) 
        #set 
        n.knob('name').setValue("Modify")

        #zoom in
        nuke.zoomToFitSelected()    

        # revert to previous selection 
        n['selected'].setValue(False) 
        for node in selNodes: 
            node['selected'].setValue(True) 
          
        return n

    #define whether the user created a node inside or outside the BD 
    def nodeInBD(self):
        createdNode = nuke.thisNode()

        def get_DAG():
            stack = QtWidgets.QApplication.topLevelWidgets()
            while stack:
                widget = stack.pop()
                if widget.objectName() == 'DAG.1':
                    widget.children()
                    for c in widget.children():
                        if isinstance(c, QtOpenGL.QGLWidget):
                            return c
                stack.extend(c for c in widget.children() if c.isWidgetType())
        
        def cursorDAGcord():
            dag_widget = get_DAG()
            dag_size = dag_widget.geometry()
            dag_center = QtCore.QPoint(dag_size.width()/2, dag_size.height()/2)
            pos = QtGui.QCursor().pos()
            pos = dag_widget.mapFromGlobal(pos)
            offset_from_center = pos - dag_center
            center = nuke.center()
            
            nodeXpos = center[0] + (offset_from_center.x() / nuke.zoom())
            nodeYpos = center[1] + (offset_from_center.y() / nuke.zoom())
            return(nodeXpos, nodeYpos)
        
        x,y = cursorDAGcord()

        #Find backdrop dimensions in DAG
        bg = nuke.toNode("Modify")
        bgx1 = bg.xpos()
        bgy1 = bg.ypos()
        bgx2 = bgx1 + bg.screenWidth()
        bgy2 = bgy1 + bg.screenHeight()

        if x > bgx1 and x< bgx2 and y > bgy1 and y < bgy2:
            pass
        else:
            nuke.delete(createdNode)
            bg.knob('selected').setValue(True)
            nuke.zoomToFitSelected()
            bg.knob('selected').setValue(False)
            a = nuke.ask('You have created a node outside the modification area. Would you like to close and save current modification?')
            if a:
                self.modifyScript()
   
    def saveNewSrcipt(self):
        item = nuke.getInput("Enter name:", "")
        if self.listWidget.findItems(item, QtCore.Qt.MatchRecursive):
            nuke.message("Specified name already exists")
        elif item == '' or item == None:
            pass
        else:
            if item != None:
                self.addToolToList(item, 'tool')
            fullPath = self.getFullPathWithExt()
            if fullPath != None: 
                nuke.nodeCopy(fullPath["path"] + item + fullPath["ext"])

    def loadScriptfromList(self):
        itemName = self.getItemName('tool')
        fullPath = self.getFullPathWithExt()
        if fullPath != None: 
            nuke.nodePaste(fullPath["path"] + itemName + fullPath["ext"])

    #get ToolSet name
    def getItemName(self, type):
        if type == 'tool':
            selectedItemList = self.listWidget.selectedItems()
            selectedItem = selectedItemList[0]
            itemName = selectedItem.text()
        elif type == 'cat':
            itemName = self.comboBox.currentText()

        return itemName
    
    #load ToolSets from NodeBoard folder in /.nuke
    def loadTools(self):
        self.listWidget.clear()
        fullPath = self.getFullPathWithExt()
        if fullPath != None: 
            nodesList = os.listdir(str(fullPath["path"]))
            ext = fullPath["ext"]
            if len(nodesList) > 0:
                for item in nodesList:
                    if item.split('.')[1] != 'json':
                        item = item[:-int(len(ext))]
                        self.addToolToList(item, 'tool')

    #load all category folders from /NodeBoard    
    def loadCategories(self):
        catList = next(os.walk(self.currentDir))[1]
        if len(catList) > 0:
                for item in catList:
                    if item != '__pycache__' and item != 'icons' and self.comboBox.findText(item) == -1:
                        self.addToolToList(item, 'cat')

    #create a new folder inside /NodeBoard
    def createNewCat(self):
        self.listWidget.clear()
        item = nuke.getInput("Enter name:", "")
        if self.comboBox.findText(item) != (-1):
            nuke.message("Specified name already exists")
            return(False)
        elif item == '' or item == None:
            return(False)
        else:
            if item != None:
                self.addToolToList(item, "cat")
                os.mkdir(self.currentDir + os.path.sep + item)
                self.changeCurrentCat(item)
                with open(self.currentDir +self.currentCat  + 'buttons.json', 'w'):
                    data = {'userButtons': []}
                    self.writeJson(data)
                self.comboBox.setCurrentText(item)
                self.changeCurrentCat(item)
                self.switchCat()
                self.preferences.updatePreferences()
                return(True)
    
    #change the current category variable
    def changeCurrentCat(self,cat):
        self.currentCat = os.path.sep  + cat + os.path.sep
    
    #change the ToolSet area based on the currently selected category
    def switchCat(self):        
        item = self.getItemName('cat')
        self.changeCurrentCat(item)
        self.loadTools()
        
        while self.userButtonLayout.count():
            child = self.userButtonLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.loadNBButtonsJSON()
        self.loadCategories()

    #update default category from preferences    
    def updateDefaultCategory(self):
        self.defaultCategory = self.preferences.preferencesNode.knob('nodeboardDefaultCategory').value()
        return self.defaultCategory

    #delete the category folder from /NodeBoard
    def deleteCategory(self):
        self.updateDefaultCategory()
        if self.defaultCategory != self.comboBox.currentText():
            if nuke.ask('Are you sure you want to delete this?'):
                self.switchCat()

                path = self.getFullPathWithExt()
                fullPath = path["path"]
                for root, dirs, files in os.walk(fullPath):
                    for file in files:
                        os.remove(os.path.join(root, file))
                os.rmdir(fullPath)

                item = 0               
                for item in range(self.comboBox.count()):
                    if self.comboBox.currentText() == self.comboBox.itemText(item):
                        self.comboBox.removeItem(item)
                    item = item + 1
                self.comboBox.setCurrentIndex(0)
 
                self.preferences.updatePreferences()
        else:
            nuke.message("You cannot modify the default category")

    #rename the cat folder in /NodeBoard
    def renameCategory(self):
        self.updateDefaultCategory()
        if self.defaultCategory != self.comboBox.currentText():
            newCatName = nuke.getInput('Enter new name:')
        
            if self.comboBox.findText(newCatName, QtCore.Qt.MatchRecursive) != -1:
                nuke.message("Specified name already exists")
            else:
                #remove from OS
                oldPath = self.currentDir + self.currentCat
                newPath = self.currentDir + os.path.sep + newCatName
                try:
                    os.rename(oldPath, newPath)
                except:
                    nuke.message("Error! try relaunching Nuke.")
                
                
                self.changeCurrentCat(newCatName)
                #remove the old item from combobox
                item = 0               
                for item in range(self.comboBox.count()):

                    
                    if self.comboBox.currentText() == self.comboBox.itemText(item):
                        self.comboBox.removeItem(item)
                    item = item + 1
                
                #switch the newly renamed item in combobox
                self.comboBox.setCurrentText(newCatName)
                self.switchCat()             
                self.preferences.updatePreferences()
        else:
            nuke.message("You cannot modify the default category")

    #share the currently selected category to the server location
    def shareCategory(self):
        self.shareLocation = Preferences().preferencesNode.knob('nodeboardShareLocation').value()
        self.emptyShareLocation(self.shareLocation)
        for root, dirs, files in os.walk(self.currentDir + self.currentCat):
            if self.shareLocation == '':
                nuke.message('Please specify the save location in the Preferences-Nodeboard first!')
            else:
                for file in files:
                    shutil.copy(os.path.join(root, file), self.shareLocation)
                
   
    #get the currently selected category from the server location
    def getCategory(self):
        dir = os.listdir(self.shareLocation)
        if len(dir) == 0:
            nuke.message('Share location is empty.')
        else:
            if self.createNewCat():
                for root, dirs, files in os.walk(self.shareLocation):
                    for file in files:
                        shutil.copy(os.path.join(root, file), self.currentDir + self.currentCat)
                self.emptyShareLocation(self.shareLocation)
                self.switchCat()

    #sync ToolSet or a Category into the W_hotbox
    def syncToHotbox(self, token = None):
        #get the path of W_hotbox from the preferences knob
        try:
            hotboxAllPath =  Preferences().preferencesNode.knob('hotboxLocation').value() +  os.path.sep + 'All' + os.path.sep
        except:
            nuke.message('''Could not find W_hotbox directory please install the latest version 
            here: https://www.nukepedia.com/python/ui/w_hotbox''')

        if hotboxAllPath != '' or hotboxAllPath != None:
            cat = self.currentCat.split(os.path.sep)[1]
            
            #find the next button position from W_hotbox
            buttonList = list()
            for button in os.listdir(hotboxAllPath):
                fileName = re.findall('[0-9]+', button)
                buttonList.append(fileName)
            
            buttonList.sort()

            lastPosition = buttonList[-1][0]
            nextPosition = str(int(lastPosition.lstrip('0')) + 1).zfill(3)

            if token == 'cat':
                #create a button in W_hotbox(newDIr)
                newDir = hotboxAllPath + os.path.sep + nextPosition
                os.mkdir(newDir)            

                #add a _name.json file from which W_hotbox reads buttons text
                currentFile = open(newDir + os.path.sep + '_name.json', 'w')
                currentFile.write(cat)
                currentFile.close() 

                #create file header from W_hotbox for .py files and add code that pastes the script to DAG
                for root, dirs, files in os.walk(self.currentDir + self.currentCat):
                    for file in files:
                        fileName = file.split('.')[0]
                        ext = file.split('.')[1]
                        if  ext != 'json':

                            dividerLine = '-'*106

                            fullPath = "'" + os.path.join(root, file) + "'"
                            nukeFullPath =  '/'.join(fullPath.split(os.path.sep))

                            s = "'" + "%clipboard%" +  "'"

                            with open(os.path.join(root, file), 'r') as file:
                                data = "'''" + file.read() + "'''"
                            

                            text = ['#%s'%dividerLine,
                                    '#',
                                    '# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX',
                                    '#',
                                    '# NAME: %s'%fileName,
                                    '#',
                                    '#%s\n\n'%dividerLine,
                                    'text= %s'%data,
                                    'clipboard= %s'%s,
                                    'cb = QtWidgets.QApplication.clipboard()',
                                    'cb.clear(mode=cb.Clipboard )',
                                    'cb.setText(text, mode= cb.Clipboard)',
                                    'nuke.nodePaste(clipboard)']
                            
                            data = '\n'.join(text)
                            currentFile = open(newDir + os.path.sep + fileName + '.py', 'w')
                            currentFile.write(data)
                            currentFile.close()
            else:
                dividerLine = '-'*106
                itemName = self.getItemName('tool')
                path = self.getFullPathWithExt()
                fullPath = "'"  + path["path"] + itemName + path["ext"] + "'"
                nukeFullPath =  '/'.join(fullPath.split(os.path.sep))
                text = ['#%s'%dividerLine,
                        '#',
                        '# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX',
                        '#',
                        '# NAME: %s'%itemName,
                        '#',
                        '#%s\n\n'%dividerLine,
                        'path= %s'%nukeFullPath,
                        'nuke.nodePaste(path)']
                
                data = '\n'.join(text)
                currentFile = open(hotboxAllPath + os.path.sep + nextPosition + '.py', 'w')
                currentFile.write(data)
                currentFile.close()               

                        
        else:
            nuke.message('Could not find W_hotbox directory please  specify the tools location in preferences')
        nuke.message('You have succesfully added ' + cat + ' to W_hotbox. Open the hotbox manager to continue')

    def setDefaultItem(self):
        self.comboBox.setCurrentText(self.defaultCategory)

    #load color pick buttons in mainMenu widget
    def loadColourPickButtons(self):
        with open(self.currentDir + os.path.sep + 'buttons.json') as f:
            data = json.load(f)
        
        for attribute in data["buttons"]:
            if attribute['name'] == "custom":                
                button = QtWidgets.QPushButton(str(attribute['title']), self.colourWidget1)
                button.clicked.connect(self.createButtonfromCustomColor)
                button.setToolTip('Creates a button inside nodeboard with the specified color')       
            else:
                button = QtWidgets.QPushButton(self.colourWidget1)
                button.setStyleSheet("background-color: " + str(attribute['color']))
                button.clicked.connect(self.createButtonFromColor)
                button.setToolTip('Creates a button inside nodeboard with the specified color') 
            
            button.setMinimumSize(QtCore.QSize(50,20))
            button.setMaximumSize(QtCore.QSize(50,20))
                        
            layoutLimit = 6
            if self.colorButtonmainMenuLayout1.count() < layoutLimit:
                self.colorButtonmainMenuLayout1.addWidget(button)
            else:
                self.colorButtonmainMenuLayout2.addWidget(button)
    
    #add a Tool to list widget
    def addToolToList(self,item, type):
        if type == 'tool':
            listWidget = self.listWidget
            nodeName = QtWidgets.QListWidgetItem("%s" % item)
            listWidget.addItem(nodeName)
        elif type == 'cat':
            self.comboBox.addItem(item)          

    ################################################################################
    # DRAG AND DROP
    ################################################################################

    def get_index(self, pos):
        for i in range(self.userButtonLayout.count()):
            buttonGlob = self.userButtonLayout.itemAt(i).widget().mapToGlobal(QtCore.QPoint(0,0)) 
            if QtCore.QRect(buttonGlob.x(), buttonGlob.y(), 80, 23).contains(pos) and i != self.target:
                return i
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:           
            self.target = self.get_index(QtGui.QCursor.pos())
        else:
            self.target = None
    
    def mouseMoveEvent(self, event):        
        if event.buttons() & QtCore.Qt.MiddleButton and self.target is not None:
            drag = QtGui.QDrag(self.userButtonLayout.itemAt(self.target).widget())
            pix = self.userButtonLayout.itemAt(self.target).widget().grab()
            mimedata = QtCore.QMimeData()
            mimedata.setImageData(pix)
            drag.setMimeData(mimedata)
            drag.setPixmap(pix)
            drag.setHotSpot(QtCore.QPoint(40,10))
            drag.exec_()
   
    def dragMoveEvent(self, event):
        cursorPos = QtGui.QCursor.pos()
        
        widgetPos = self.nodeBoardWidget.mapToGlobal(QtCore.QPoint(0,0))
        if cursorPos.x() <= widgetPos.x() or cursorPos.y() <= widgetPos.y():
           QtGui.QCursor.setPos(QtGui.QCursor.pos().x() +10 , QtGui.QCursor.pos().y() +10 )
 
    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        buttonGlob = self.userButtonLayout.itemAt(self.target).widget().mapToGlobal(self.pos())
        if not QtCore.QRect(buttonGlob.x(), buttonGlob.y(), 80, 23).contains(QtGui.QCursor.pos()):
            source = self.get_index(QtGui.QCursor.pos())
            if source is None:
                return
            i, j = max(self.target, source), min(self.target, source)
            p1, p2 = self.userButtonLayout.getItemPosition(i), self.userButtonLayout.getItemPosition(j)

            self.userButtonLayout.addItem(self.userButtonLayout.takeAt(i), *p2)
            self.userButtonLayout.addItem(self.userButtonLayout.takeAt(j), *p1)
            self.target = None
            self.renderButtons(1)
