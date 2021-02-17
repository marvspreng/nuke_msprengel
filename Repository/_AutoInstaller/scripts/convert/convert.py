###########################################################################################################
#
#  convert
#
#  @author simon Jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de
#
#  description:
#  convert read node to correct input node. This ensures that you can simply drag and drop all files from
#  your explorer to your node graph and then simply convert to the correct format
#
#      # deep data: convert read node to deep read node
#      # abc: convert read node to readgeo node
#      # fbx: convert read node to camera node
#      # obj: convert read node to readgeo node
#
#  installation:
#  put the whole convert folder into your nuke home directory
#  in your init.py write (without the '#'):
#
#  nuke.pluginAddPath("convert")
#
#  usage:
#  after installation is done simply drag and drop some files into your dag. In your menu bar you
#  will have to new commands:
#  Edit -> convert file node (guess)    --> this will try to convert to the best suitable node automatically. The
#                                           conversion node is managed by the guess list
#  Edit -> convert file node (manual)   --> this will open the convert panel to select the desired convert node manually
#
##########################################################################################################

# nodes_valid_list
# this is the list of possible conversion nodes. It will be presented when choosing the manual conversion method
#
nodes_valid_list = ["Read", "DeepRead", "ReadGeo2", "Camera2"]
#
# guess list
# set the conversion node for each type in here
guess_list = {".exr": "DeepRead",
              ".abc": "ReadGeo2",
              ".fbx": "Camera2",
              ".obj": "ReadGeo"
              }

##########################################################################################################
# no need to change anything from here. Edit only if you know exactly what you're doing.


import os
import nuke
import converthelper as helper


def show_convert_node_panel(guess=False):
    """
    show window to convert node
    :param guess: Bool if set to True guess the right convert type and don't show convert type panel
    :return: None
    """

    # get all "valid" nodes of selection, e.g. all nodes that are in nodes_valid_list
    sel = [n for n in nuke.selectedNodes() if n.Class() in nodes_valid_list]
    if len(sel) == 0:
        return

    p = nuke.Panel("convert")
    p.addEnumerationPulldown("convert to", " ".join(nodes_valid_list))

    if guess:
        # guess process conversion
        for node in sel:
            ext = os.path.splitext(node["file"].getValue())[1].lower()
            if ext in guess_list.keys():
                type_convert = guess_list[ext]
                convert_node(node, type_convert)
            else:
                return

    else:
        if p.show():
            type_convert = p.value("convert to")

        # manual process conversion
        for node in sel:
            convert_node(node, type_convert)


def convert_node(node, type_convert):
    """
    process node convert and remove old node
    :param node: Nuke node to process
    :param type_convert: String class name of new node to create
    :return: None
    """

    type_current = node.Class()

    # create convert object
    cv = helper.create_convert_node(node)
    if cv is None:
        return

    node_convert = nuke.createNode(type_convert)

    # position converted node
    node_convert.setXYpos(int(node["xpos"].getValue()), int(node["ypos"].getValue()))
    node_convert["file"].setValue(node["file"].getValue())

    # set values
    for key in cv.get_vals().keys():
        helper.paste_val(node_convert, key, cv.get_vals()[key])

    nuke.delete(node)





