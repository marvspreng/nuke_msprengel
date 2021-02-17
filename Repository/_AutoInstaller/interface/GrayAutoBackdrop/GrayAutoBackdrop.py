# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.
# Edit by Max van Leeuwen - maxvanleeuwen.com



import nuke, random
import colorsys



# color for backdrop (stacked backdrops will get darker)
startingColor = 1179010815



# make every stacked backdrop slightly darker
def darker(levels):

    newColor = startingColor

    for i in xrange( int( abs(levels) ) ):
        RGB = [(0xFF & newColor >>  i) / 255.0 for i in [24,16,8]]
        HSV = colorsys.rgb_to_hsv(RGB[0],RGB[1],RGB[2])

        newHSV = [HSV[0], HSV[1], HSV[2] * .85]
        newRGB = colorsys.hsv_to_rgb(newHSV[0],newHSV[1],newHSV[2])

        newColor = int('%02x%02x%02x%02x' % (newRGB[0]*255,newRGB[1]*255,newRGB[2]*255,255),16)

    return newColor


def nodeIsInside (node, backdropNode):

    """Returns true if node geometry is inside backdropNode otherwise returns false"""

    topLeftNode = [node.xpos(), node.ypos()]
    topLeftBackDrop = [backdropNode.xpos(), backdropNode.ypos()]
    bottomRightNode = [node.xpos() + node.screenWidth(), node.ypos() + node.screenHeight()]
    bottomRightBackdrop = [backdropNode.xpos() + backdropNode.screenWidth(), backdropNode.ypos() + backdropNode.screenHeight()]

    topLeft = ( topLeftNode[0] >= topLeftBackDrop[0] ) and ( topLeftNode[1] >= topLeftBackDrop[1] )
    bottomRight = ( bottomRightNode[0] <= bottomRightBackdrop[0] ) and ( bottomRightNode[1] <= bottomRightBackdrop[1] )

    return topLeft and bottomRight


def GrayAutoBackdrop():

    '''
    Automatically puts a backdrop behind the selected nodes.

    The backdrop will be just big enough to fit all the select nodes in, with room
    at the top for some text in a large font.
    '''
    
    
    largeLabel = False


    selNodes = nuke.selectedNodes()
    if selNodes:

        # Calculate bounds for the backdrop node.
        bdX = min([node.xpos() for node in selNodes])
        bdY = min([node.ypos() for node in selNodes])
        bdW = max([node.xpos() + node.screenWidth() for node in selNodes]) - bdX
        bdH = max([node.ypos() + node.screenHeight() for node in selNodes]) - bdY


        # bigger boundaries if node area is bigger
        boundsMult = 10 + (bdW + bdH) / 100

        zOrder = 0
        selectedBackdropNodes = nuke.selectedNodes( "BackdropNode" )
        #if there are backdropNodes selected put the new one immediately behind the farthest one
        if len( selectedBackdropNodes ) :
            zOrder = min( [node.knob( "z_order" ).value() for node in selectedBackdropNodes] ) - 1
        else :
            #otherwise (no backdrop in selection) find the nearest backdrop if exists and set the new one in front of it
            nonSelectedBackdropNodes = nuke.allNodes("BackdropNode")
            for nonBackdrop in selNodes:
                for backdrop in nonSelectedBackdropNodes:
                    if nodeIsInside( nonBackdrop, backdrop ):
                        zOrder = max( zOrder, backdrop.knob( "z_order" ).value() + 1 )
        
        # bigger label size if level 0 (or lower) backdrop, but only if boundsmult is more than 15
        if zOrder <= 0 and boundsMult > 15:
	  largeLabel = True
	  

        # Expand the bounds to leave a border, relative to zoom size. Elements are offsets for left, top, right and bottom edges respectively. Extra top height if larger label.
        left, top, right, bottom = (-10 * boundsMult, -80 - 10 * boundsMult, 10 * boundsMult, 10 * boundsMult)
        bdX += left
        bdY += top
        bdW += (right - left)
        bdH += (bottom - top) + (100 if largeLabel else 0)

        labelstr = nuke.getInput('Backdrop label', ' ')
        if labelstr:

            if labelstr[0] == ' ':
                labelstr = labelstr[1:len(labelstr)]
            n = nuke.nodes.BackdropNode(xpos = bdX,
                bdwidth = bdW,
                ypos = bdY,
                bdheight = bdH,
                tile_color = darker(zOrder),
                note_font_size = 200 if largeLabel else 42,
                z_order = zOrder,
                label = labelstr )

            # revert to previous selection
            n['selected'].setValue(False)
            for node in selNodes:
                node['selected'].setValue(True)

            return n

        else:

            pass

    else:
        pass