##############################################################################
#                                                                            #
# superAutoCrop                                                              #
# V 1.3                                                                      #
# Release December 01 2020                                                   #
#                                                                            #
# Did as a thankful gift to my mentor and friend Emerson Bonadias.           #
#                                                                            #
# Created by Luciano Cequinel (vimeo.com/cequinavfx)                         #
# to report bugs or suggestions lucianocequinel@gmail.com                    #
#                                                                            #
##############################################################################


'''

Just write
import superAutoCrop
on menu.py
and copy superAutoCrop.py to .nuke folder

See the ref_menu.py as a reference


'''

import nuke


def superAutoCrop():

    selNode = nuke.selectedNodes()
    nkRoot = nuke.root()

    if len(selNode) == 1:
        selNode = nuke.selectedNode()

        if selNode.Class == ('Read'):
            fFrame = selNode['first'].getValue()
            lFrame = selNode['last'].getValue()
            wNode = selNode.width()
            hNode = selNode.height()
        else:
            fFrame = nkRoot['first_frame'].getValue()
            lFrame = nkRoot['last_frame'].getValue()


        wNode = selNode.width()
        hNode = selNode.height()

        cTool = nuke.createNode('CurveTool')
        cTool.setInput(0, selNode)
        cTool['operation'].setValue('Auto Crop')
        cTool['channels'].setValue('alpha')
        cTool['resetROI'].setValue('True')
        cTool.knob("ROI").setValue([0,0,selNode.width(),selNode.height()])
        cTool.setInput(0, selNode)

        nuke.execute(cTool, int(fFrame), int(lFrame))

        nCrop = nuke.createNode('Crop')
        nCrop.knob("box").copyAnimations(cTool.knob("autocropdata").animations())
        nCrop['label'].setValue('AutoCrop from %s' %(selNode.name()))
        
        tab = nuke.Tab_Knob('Size Control')
        nCrop.addKnob(tab)
        
        gS = nuke.Double_Knob('genSize',"Proportional Size")
        gS.setRange(0,300)
        nCrop.addKnob(gS)

        div = nuke.Text_Knob("divider","")
        nCrop.addKnob(div)

        lS = nuke.Double_Knob('lSize',"Left")
        lS.setRange(-50,50)
        nCrop.addKnob(lS)

        rS = nuke.Double_Knob('rSize',"Right")
        rS.setRange(-50,50)
        nCrop.addKnob(rS)

        tS = nuke.Double_Knob('tSize',"Top")
        tS.setRange(-50,50)
        nCrop.addKnob(tS)
        
        bS = nuke.Double_Knob('bSize',"Bottom")
        bS.setRange(-50,50)
        nCrop.addKnob(bS)


        nCrop['genSize'].setValue(30)


        nCrop.knob('box').setExpression('(curve) + ((knob.lSize) + (knob.genSize) *-1)', 0)
        nCrop.knob('box').setExpression('(curve) + ((knob.bSize) + (knob.genSize) *-1)', 1)
        nCrop.knob('box').setExpression('(curve) + (knob.rSize) + (knob.genSize)', 2)
        nCrop.knob('box').setExpression('(curve) + (knob.tSize) + (knob.genSize)', 3)

        nCrop.knob('tile_color').setValue(01050)

        nuke.delete(cTool)


    else:
        nuke.message('Select one node, please!')

