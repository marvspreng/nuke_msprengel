try:
    from PySide import QtWidgets, QtCore
except ImportError:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from PySide2 import QtGui
    from PySide2 import QtOpenGL

import os
import string



class QLabelButton(QtWidgets.QLabel):

    '''
    Custom class to make a Qlabel function as a button.

    Copyright (c) 2016-2021, Wouter Gilsing
    All rights reserved.
    '''

    #signals
    clicked = QtCore.Signal()

    def __init__(self,name,linkedWidget = None):
        super(QLabelButton, self).__init__()

        self.linkedWidget = linkedWidget

        self.currentDir = os.path.dirname(os.path.realpath(__file__))
        iconFolder = self.currentDir + os.path.sep + 'icons'

        while iconFolder[-1] == '/':
            iconFolder = iconFolder[:-1]

        self.imageFile = '%s/hotbox_%s'%(iconFolder,name)

        #check if icon is present. If not, display '?'
        if not os.path.isfile('%s_neutral.png'%self.imageFile):
            self.imageFile = None

            self.setText('<font size = "6">?</font>')
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setStyleSheet('color: #717171')

        #add image
        else:
            self.updateIcon()

        #format name
        if name != name.lower():

            newName = ''

            for character in  name:
                if character in string.ascii_uppercase:
                    character = ' ' + character.lower()
                newName = newName + character

            name = newName

        #tooltip
        self.setToolTip(name)

    #--------------------------------------------------------------------------------------------------
    #Events
    #--------------------------------------------------------------------------------------------------

    def enterEvent(self, event):
        self.updateIcon('hover')

    def leaveEvent(self,event):
        self.updateIcon()

    def mousePressEvent(self,event):
        self.updateIcon('clicked')

    def mouseReleaseEvent(self,event):
        #emit signal

        self.updateIcon('hover')

        #if button has a linkedwidget set, check if that widget is enabled.
        #if not, dont emit clicked signal

        self.clicked.emit()

    #--------------------------------------------------------------------------------------------------

    def updateIcon(self, mode = 'neutral'):

        if self.imageFile:
            path = '%s_%s.png'%(self.imageFile,mode)
            self.setPixmap(QtGui.QPixmap(path))

#custom separator line widget
class QHLine(QtWidgets.QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)

#custom dropdown menu widget
class Collapse(QtWidgets.QWidget):
    def __init__(self, parent = None, title=None):
        super(Collapse, self).__init__(parent)

        self._is_collasped = True
        self._title_frame = None
        self._content, self._content_layout = (None, None)

        self._main_v_layout = QtWidgets.QVBoxLayout(self)
        self._main_v_layout.addWidget(self.initTitleFrame(title, self._is_collasped))
        self._main_v_layout.addWidget(self.initContent(self._is_collasped))

        self.initCollapsable()

    def initTitleFrame(self, title, collapsed):
        self._title_frame = TitleFrame(title=title, collapsed=collapsed)

        return self._title_frame

    def initContent(self, collapsed):
        self._content = QtWidgets.QWidget()
        self._content_layout = QtWidgets.QVBoxLayout()

        self._content.setLayout(self._content_layout)
        self._content.setVisible(not collapsed)

        return self._content

    def addWidget(self, widget):
        self._content_layout.addWidget(widget)

    def initCollapsable(self):
        QtCore.QObject.connect(self._title_frame, QtCore.SIGNAL('clicked()'), self.toggleCollapsed)

    def toggleCollapsed(self):
        self._content.setVisible(self._is_collasped)
        self._is_collasped = not self._is_collasped
        self._title_frame._arrow.setArrow(int(self._is_collasped))

class TitleFrame(QtWidgets.QFrame):
    def __init__(self, parent=None, title="", collapsed=False):
        QtWidgets.QFrame.__init__(self, parent=parent)

        self.setMinimumHeight(24)
        self.move(QtCore.QPoint(24, 0))
        self.setStyleSheet("border:1px solid #292929;")

        self._hlayout = QtWidgets
        self._hlayout = QtWidgets.QHBoxLayout(self)
        self._hlayout.setContentsMargins(0, 0, 0, 0)
        self._hlayout.setSpacing(0)

        self._arrow = None
        self._title = None

        self._hlayout.addWidget(self.initArrow(collapsed))
        self._hlayout.addWidget(self.initTitle(title))

    def initArrow(self, collapsed):
        self._arrow = Arrow(collapsed=collapsed)
        self._arrow.setStyleSheet("border:0px")

        return self._arrow

    def initTitle(self, title=None):
        self._title = QtWidgets.QLabel(title)
        self._title.setMinimumHeight(24)
        self._title.move(QtCore.QPoint(24, 0))
        self._title.setStyleSheet("border:0px")

        return self._title

    def mousePressEvent(self, event):
        self.emit(QtCore.SIGNAL('clicked()'))

        return super(TitleFrame, self).mousePressEvent(event)    


class Arrow(QtWidgets.QFrame):
    def __init__(self, parent=None, collapsed=False):
        QtWidgets.QFrame.__init__(self, parent=parent)

        self.setMaximumSize(24, 24)

        # horizontal == 0
        self._arrow_horizontal = (QtCore.QPointF(7.0, 8.0), QtCore.QPointF(17.0, 8.0), QtCore.QPointF(12.0, 13.0))
        # vertical == 1
        self._arrow_vertical = (QtCore.QPointF(8.0, 7.0), QtCore.QPointF(13.0, 12.0), QtCore.QPointF(8.0, 17.0))
        # arrow
        self._arrow = None
        self.setArrow(int(collapsed))

    def setArrow(self, arrow_dir):
        if arrow_dir:
            self._arrow = self._arrow_vertical
        else:
            self._arrow = self._arrow_horizontal

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setBrush(QtGui.QColor(192, 192, 192))
        painter.setPen(QtGui.QColor(64, 64, 64))
        painter.drawPolygon(self._arrow)
        painter.end()