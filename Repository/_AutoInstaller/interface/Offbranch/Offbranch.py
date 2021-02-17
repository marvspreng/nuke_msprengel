# Max van Leeuwen - maxvanleeuwen.com
# Offbranch - 1.0
#
# This will move the selected node to a new branch in the stream.


import nuke


def Offbranch():

	try:

		xoffs = 150
		yoffs = 50

		
		# get nodes
		n = nuke.selectedNode()
		i = n.dependencies()[0]
		o = None

		
		# try to find the output node
		outp = False

		try:
			o = n.dependent()[0]
			outp = True

		except Exception as e:
			pass

		
		# get node size/position
		nxs = n.screenWidth()
		nys = n.screenHeight()
		nxp = n.xpos() + nxs/2
		nyp = n.ypos() + nys/2


		
		# first dot (in-stream)
		d1 = nuke.Nodes().Dot()
		d1xs = d1.screenWidth()
		d1ys = d1.screenHeight()

		d1['xpos'].setValue(nxp - d1xs/2)
		d1['ypos'].setValue(nyp - d1ys/2)

		
		# second dot (out of stream)
		d2 = nuke.Nodes().Dot()
		d2xs = d2.screenWidth()
		d2ys = d2.screenHeight()

		d2['xpos'].setValue(nxp + nxs/2 + xoffs - d2xs/2)
		d2['ypos'].setValue(nyp - d2ys/2)

		
		# set node position
		n['xpos'].setValue(nxp + xoffs)
		n['ypos'].setValue(nyp + yoffs)

		
		# reconnect
		d2.setInput(0, d1)
		d1.setInput(0, i)
		n.setInput(0, d2)

		if(outp):
			o.setInput(0, d1)

	except Exception as e:
		pass


# autostart (if not imported)
if __name__ == "__main__":
	Offbranch()