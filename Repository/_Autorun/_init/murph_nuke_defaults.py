################
##knobdefaults##
################

#project settings
nuke.addFormat ("3840 2160 0 0 3840 2160 1.0 Glitch HD")
nuke.addFormat ("1920 1080 0 0 1920 1080 1.0 FullHD")
nuke.knobDefault("Root.format", "Glitch HD")
nuke.knobDefault("Root.first_frame", "1001")
nuke.knobDefault("Root.last_frame", "2000")
nuke.knobDefault("Root.fps", '25')
nuke.knobDefault("Viewer.fps", "25")


#Colorspace
nuke.knobDefault("Read.cached", "1")
nuke.knobDefault("Read.cacheLocal", "always")

# RotoPaint
nuke.knobDefault("RotoPaint.toolbox", "brush {{brush ltt 0} {clone ltt 0}}")
nuke.knobDefault("RotoPaint.toolbox", '''clone {
{ brush opc 0.2}
{ clone opc 0.2}
}''')
nuke.knobDefault("RotoPaint.feather_type", "smooth")
nuke.knobDefault("Roto.feather_type", "smooth") 
nuke.knobDefault("Bezier.output","alpha")
nuke.knobDefault("Bezier.linear","on")

#Labels
nuke.knobDefault('VectorDistort.label', 'ref frame [value referenceFrame]')
nuke.knobDefault('Tracker.label', '[value transform] <br> ref frame: [value reference_frame]')
nuke.knobDefault('Constant.label', '[value width] x [value height]')
nuke.knobDefault('TimeClip.label', '[value first] to [value last]')
nuke.knobDefault('OCIOColorSpace.label', '<i>[value in_colorspace]</i> <b>to</b> <i>[value out_colorspace]')
nuke.knobDefault('Switch.label', '[value which]')
nuke.knobDefault('Dissolve.label', '[value which]')
nuke.knobDefault("Blur.label","[value size]")
nuke.knobDefault("TimeOffset.label", "[value time_offset]")

nuke.knobDefault("Merge.label", "[if {[value mix]<1} { value mix }]")
nuke.knobDefault("Saturation.label", "[if {[value saturation]<1} { value saturation }]")
nuke.knobDefault('Mirror2.flop', 'True')
nuke.knobDefault("TimeBlur.shutteroffset","centred")
nuke.knobDefault("MotionBlur2D.shutteroffset","centred")
nuke.knobDefault("MotionBlur3D.shutteroffset","centred")
nuke.knobDefault("Grade.black_clamp","0")

#Misc
nuke.knobDefault('LayerContactSheet.showLayerNames', '1')
nuke.addOnUserCreate(lambda:nuke.thisNode()['first_frame'].setValue(nuke.frame()), nodeClass='FrameHold')
nuke.knobDefault( "Grade.black_clamp" , "false" ) 
nuke.knobDefault('STMap.uv', 'rgba')
nuke.knobDefault("EXPTool.mode", "0")
nuke.knobDefault("StickyNote.note_font_size", "50")
nuke.knobDefault("ScanlineRender.motion_vectors_type", "off")
nuke.knobDefault("ScanlineRender.MB_channel", "none")
nuke.knobDefault("FilterErode.channels","alpha")
nuke.knobDefault('Tracker.reference_frame', '1001')

#bbox
nuke.knobDefault("Merge.bbox", "3")

# NO CLIPS
nuke.knobDefault("Project3D.crop", "0")
nuke.knobDefault("Roto.cliptype","no clip")
nuke.knobDefault("RotoPaint.cliptype","no clip")
nuke.knobDefault("Grid.cliptype","no clip")
nuke.knobDefault("Noise.cliptype","no clip")
nuke.knobDefault("Radial.cliptype","no clip")
nuke.knobDefault("Rectangle.cliptype","no clip")
nuke.knobDefault("Ramp.cliptype","no clip")
nuke.knobDefault("Text2.cliptype","no clip")

#conveniant
nuke.knobDefault("LensDistortion.gridType", "Thin Line")
nuke.knobDefault("CheckerBoard.centerlinewidth","0")

#Viewer
nuke.knobDefault("Viewer.freezeGuiWhenPlayBack", "1")  




