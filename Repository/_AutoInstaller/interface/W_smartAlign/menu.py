import W_smartAlign

menuBar = nuke.menu("Nuke")
menuBar.addCommand("Edit/Node/Align/Left", 'W_smartAlign.alignNodes("left")', "#+left", shortcutContext=2)
menuBar.addCommand("Edit/Node/Align/Right", 'W_smartAlign.alignNodes("right")', "#+right", shortcutContext=2)
menuBar.addCommand("Edit/Node/Align/Up", 'W_smartAlign.alignNodes("up")', "#+up", shortcutContext=2)
menuBar.addCommand("Edit/Node/Align/Down", 'W_smartAlign.alignNodes("down")', "#+down", shortcutContext=2)

