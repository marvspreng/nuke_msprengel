import convertnode as c


def paste_val(node, knob_name, knob_value):
    """
    paste knob_value into new node
    @param node: Nuke node to process
    @param knob_name: String knob name to fill
    @param knob_value: String knob val to set
    :return: None
    """

    if node.knob(knob_name) is not None:
        node.knob(knob_name).setValue(knob_value)


def create_convert_node(node):
    """
    read data from given node, create and fill ConvertNode object and return it
    :param node: Nuke node to read and process
    :return: ConvertNode convert node object
    """

    try:
        file = read_knob_val(node, "file").getValue()
        first = int(read_knob_val(node, "first").getValue())
        last = int(read_knob_val(node, "last").getValue())
        first2 = int(read_knob_val(node, "origfirst").getValue())
        last2 = int(read_knob_val(node, "origlast").getValue())
        format = read_knob_val(node, "format").value()
    except Exception, e:
        return None

    cv = c.ConvertNode(file, first, last, first2, last2, format)
    return cv


def read_knob_val(node, knob_name):
    """
    try to read the knob value; if it doesn't exist return empty String
    :return: Strign knob value
    """

    try:
        return node[knob_name]
    except KeyError:
        return ""
    except NameError:
        return ""



