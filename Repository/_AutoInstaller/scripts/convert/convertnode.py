class ConvertNode(object):
    """
    convert node container containing
    all necessary knobs to tmp store
    """

    def __init__(self, file, first, last, first2, last2, format):

        self.file = file
        self.first = first
        self.last = last
        self.first2 = first2
        self.last2 = last2
        self.format = format

        self.vals = {"file": self.file,
                     "first": self.first,
                     "last": self.last,
                     "first2": self.first2,
                     "last2": self.last2,
                     "format": self.format
                     }

    def get_vals(self):
        return self.vals


