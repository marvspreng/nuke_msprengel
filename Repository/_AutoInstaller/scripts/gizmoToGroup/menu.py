#turn Gizmos into groups so you can transfer to any nuke, that has not installed theses gizmos
import gizmoToGroup
nuke.menu("Nuke").addCommand('Marv/gizmoToGroup', 'gizmoToGroup.replaceGizmoWithGroup()', 'ctrl+g')