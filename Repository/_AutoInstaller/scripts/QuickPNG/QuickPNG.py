# Exports a PNG file to the desktop for each selected node (file name: 'Desktop/[Script name]_[Node name]_[Frame number]_[Date (%Y-%M-%D-%H-%M-%S)].png')
# QuickPNG v1.2 - Max van Leeuwen - https://maxvanleeuwen.com/downloads/#QuickPNG

import os
import platform
from datetime import datetime

if platform.system() == "Windows":
	desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop').replace("\\", "/")
else: # Linux, Unix
	desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/QuickPNG').replace("\\", "/")

def ask(amount):
	start = nuke.ask('Are you sure you want to write ' + str(amount) + ' PNG files to your desktop?')
	if start:
		return 1

def WriteFromNode(CurrNode): # This does the actual work
	CurrFileIndex = 1
	CompName = os.path.splitext(os.path.basename(nuke.root().knob('name').value()))[0]
	CurrComp = CompName if CompName is not "" else "untitled"
	CurrTime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
	CurrFrame = int(nuke.knob("frame"))

	filename = ""
	if os.path.exists(desktop + "/" + CurrComp + "_" + CurrNode.name() + "_" + (str)(CurrFrame) + "_" + CurrTime + ".png"):
		while os.path.exists(desktop + "/" + CurrComp + "_" + CurrNode.name() + "_" + (str)(CurrFrame) + "_" + CurrTime + "_" + str(CurrFileIndex).zfill(4) + ".png"):
		    CurrFileIndex += 1
		filename = desktop + "/" + CurrComp + "_" + CurrNode.name() + "_" + (str)(CurrFrame) + "_" + CurrTime + "_" + str(CurrFileIndex).zfill(4) + ".png"
	else:
		filename = desktop + "/" + CurrComp + "_" + CurrNode.name() + "_" + (str)(CurrFrame) + "_" + CurrTime + ".png"

	write1 = nuke.nodes.Write(file = filename, name='TEMP_WRITE_1' , file_type='png', channels='rgba')
	write1.setInput(0, CurrNode)

	nuke.execute(write1.name(), CurrFrame, CurrFrame)

	nuke.delete(write1)
	CurrNode.setSelected(True)

	print ("[QuickPNG] Exported node " + CurrNode.name() + " to " + filename)

def QuickPNG():
	SelectedNodes = nuke.selectedNodes()
	amount = len(SelectedNodes)
	if (amount == 1): # If one node is selected
		CurrNode = nuke.selectedNode()
		WriteFromNode(CurrNode)	
	elif (amount > 1): # If multiple nodes are selected
		if ask(amount):
			for CurrNode in SelectedNodes:
				WriteFromNode(CurrNode)
	else:
		print("[QuickPNG] No node(s) selected!")

QuickPNG()