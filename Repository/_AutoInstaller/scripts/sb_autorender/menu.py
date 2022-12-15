import sb_autoRender


nuke.toolbar("Nodes").addCommand("murph/render/sb AutoRender", '''sb_autoRender.sb_autoRenderNode(
		rootFolderMethod="search word",
		rootFolderUserInput="work", 
		customRenderPath="",
		renderType="main render",
		renderName="script name",
		customName="",
		prefix="",
		suffix="",
		addSubfolder=True,
		addColorspaceSubfolder=False,
		addFileExtensionSubfolder=False,
		addColorToFileName=False,
		useOCIO=False,
		channels="rgba",
		colorspace="default",
		fileType="exr",
		mainRenderFolder="OUT/render",
		precompRenderFolder="OUT/prerender",
		proxyRenderFolder="OUT/preview",
		framePaddingSep=".",
		framePadding="####"
		)''', "shift+w")
        

"""
	You also have the option to set default values to most of the knobs depending on your pipeline.
	The syntax for adding a custom version of sb_autoWrite:
	<menu-bar>.addCommand("<name in menu>", 'sb_autoRender.sb_autoRenderNode(<root folder method>, <user input (search word/environment variables)>, <custom path>, <render name>, <custom name>, <add subfolder>, <render type>, <prefix>, <suffix>, <add colorspace to filename>, <use OCIO for color conversions>, <channels>, <colorspace>, <file extension>, <main render folder>, <precomp render folder>, <proxy render folder>, <framepadding separator (._-)>, <framepadding (#)> )', '')
	Note that the environment variable USE_OCIO (set to "1") will override the useOCIO argument.
	Most of the string knobs (exluding the rootFolderUserInput knob) can be written as TCL expressions and evaluated at rendertime. For example you could add _[value channels] to write the channels as a suffix.
"""