# -*- coding: utf-8 -*-
"""
/***************************************************************************
 quickcrsDialog
                                 A QGIS plugin
 One click to enable your favourite CRS (OTF)
                             -------------------
        begin                : 2017-02-06
        copyright            : (C) 2017 by Michel Stuyts
        email                : info@stuyts.xyz
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
try:
    from qgis.PyQt.QtCore import *
except ImportError:
    from PyQt4.QtCore import *
try:
    from qgis.PyQt import uic
except ImportError:
    from PyQt4 import uic
try:
    from qgis.PyQt.QtGui import QIcon
    from qgis.PyQt.QtWidgets import QDialog
except ImportError:
    from PyQt4.QtGui import QIcon, QDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'quickcrs_dialog_base.ui'))


class quickcrsDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(quickcrsDialog, self).__init__(parent)
        self.resize(QSize(400, 230).expandedTo(self.minimumSizeHint()))
        self.setWindowIcon(QIcon(":/plugins/QuickCRS/icon.png"))
        self.setWindowFlags( self.windowFlags() & ~Qt.WindowContextHelpButtonHint |  Qt.CustomizeWindowHint  | Qt.WindowTitleHint  )
        self.setupUi(self)
