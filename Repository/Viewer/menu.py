
#############################
# set points position values  on format change
#############################

def InitialPPValues():

    w = int (nuke.root().knob('format').value().width())
    h = int (nuke.root().knob('format').value().height())
    wHalf = int (w/2)
    hHalf = int (h/2)


    iPP = nuke.thisNode()
    iPP[ 'origine' ].setValue( [wHalf, hHalf] )
    iPP[ 'punto1T_User' ].setValue( [w + 30, h + 30] )
    iPP[ 'punto2T_User' ].setValue( [w + 30 , hHalf] )
    iPP[ 'punto3T_User' ].setValue( [w + 30 , - 30] )
    iPP[ 'punto4T_User' ].setValue( [- 30, - 30] )
    iPP[ 'punto5T_User' ].setValue( [- 30, hHalf] )
    iPP[ 'punto6T_User' ].setValue( [- 30,h + 30] )

nuke.addOnUserCreate( InitialPPValues, nodeClass='breakdownDesignTool')


# AUTOMATED VIEWER FRAME HANDLES
# Add this code to the Menu.py file in your .nuke directory

# This code adds commands for 24, 12, and 8 frame handles.
# If you don't need all of them, you can delete the function
# and nuke.menu addCommand for that frame range.


# 24 Frame Handles

def newViewerRange24():
  # Get the node that is the current viewer
  v = nuke.activeViewer().node()
  # Get the first and last frames from the project settings
  firstFrame = nuke.Root()['first_frame'].value()
  lastFrame = nuke.Root()['last_frame'].value()
  # get a string for the new range and set this on the viewer
  newRange = str(int(firstFrame)+24) + '-' + str(int(lastFrame) - 24)
  v['frame_range_lock'].setValue(True)
  v['frame_range'].setValue(newRange)


# 12 Frame Handles

def newViewerRange12():
  # Get the node that is the current viewer
  v = nuke.activeViewer().node()
  # Get the first and last frames from the project settings
  firstFrame = nuke.Root()['first_frame'].value()
  lastFrame = nuke.Root()['last_frame'].value()
  # get a string for the new range and set this on the viewer
  newRange = str(int(firstFrame)+12) + '-' + str(int(lastFrame) - 12)
  v['frame_range_lock'].setValue(True)
  v['frame_range'].setValue(newRange)


# 8 Frame Handles

def newViewerRange8():
  # Get the node that is the current viewer
  v = nuke.activeViewer().node()
  # Get the first and last frames from the project settings
  firstFrame = nuke.Root()['first_frame'].value()
  lastFrame = nuke.Root()['last_frame'].value()
  # get a string for the new range and set this on the viewer
  newRange = str(int(firstFrame)+8) + '-' + str(int(lastFrame) - 8)
  v['frame_range_lock'].setValue(True)
  v['frame_range'].setValue(newRange)

# Adding the commands to the Viewer Menu
viewerbar = nuke.menu("Nuke").findItem("Viewer")
viewerbar.addSeparator()
nuke.menu('Nuke').addCommand('Viewer/Viewer Handles - 24f',
"newViewerRange24()")
nuke.menu('Nuke').addCommand('Viewer/Viewer Handles - 12f',
"newViewerRange12()")
nuke.menu('Nuke').addCommand('Viewer/Viewer Handles - 8f',
"newViewerRange8()")



# NODE SETS v1.1
# Add this code to the Menu.py file in your .nuke directory

# This function opens the control panels of
# all the nodes with "inNodeSet" on their label

def showOnlyChosenNodes():
  names = []
  li = []
  for node in nuke.allNodes():
    if "inNodeSet" in node['label'].value():
      names.extend([node.name()])
      li.extend([node])
  numPan = nuke.toNode('preferences')['maxPanels']
  numPan.setValue(len(names))
  for i in range(len(li)):
    node = li[i]
    node.showControlPanel()

# This function adds "inNodeSet" to a
# new line on the label of all the selected nodes

def labelNodes():
  for node in nuke.selectedNodes():
    label = node['label'].value()
    if 'inNodeSet' not in label:
      node['label'].setValue( label +  '\ninNodeSet')

# and this one clears the label of
# all the selected nodes

def unLabelNodes():
  for node in nuke.selectedNodes():
    label = node['label'].value()
    if 'inNodeSet' in label:
      node['label'].setValue( label.replace('\ninNodeSet','') )

nuke.menu('Nuke').addCommand('Edit/Node Set: Show Nodes', 'showOnlyChosenNodes()')
nuke.menu('Nuke').addCommand('Edit/Node Set: Add Selected', 'labelNodes()')
nuke.menu('Nuke').addCommand('Edit/Node Set: Remove Selected', 'unLabelNodes()')
    


# Copy With Expressions Function and Menu Command

def CopyWithExp():
  sourceNode = nuke.selectedNode().name()
  nuke.nodeCopy("%clipboard%")
  nuke.nodePaste("%clipboard%")
  destNode = nuke.selectedNode().name()
  for i in nuke.selectedNodes():
      for j in i.knobs():
          i[j].setExpression( sourceNode + '.' + j )
      i['xpos'].setExpression('')
      i['ypos'].setExpression('')
      i['selected'].setExpression('')
      i['channels'].setExpression( sourceNode + '.channels' )


nuke.menu('Nuke').addCommand('Edit/Copy with Expressions', "CopyWithExp()", "^#C")