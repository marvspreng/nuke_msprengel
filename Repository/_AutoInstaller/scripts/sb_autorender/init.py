nuke.pluginAddPath('./python')
import sb_autoRender
nuke.addBeforeRender(sb_autoRender.sb_autoRender)