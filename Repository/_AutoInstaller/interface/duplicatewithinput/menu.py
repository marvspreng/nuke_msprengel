import duplicateWithInputs
nuke.menu('Nuke').addCommand('Edit/Duplicate with Inputs/copy','duplicateWithInputs.copyWithInputs()', '#+c')
nuke.menu('Nuke').addCommand('Edit/Duplicate with Inputs/paste','duplicateWithInputs.pasteWithInputs()', '#+v')
nuke.menu('Nuke').addCommand('Edit/Duplicate with Inputs/duplicate','duplicateWithInputs.duplicateWithInputs()', '#+x')