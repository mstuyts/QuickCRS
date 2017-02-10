# -*- coding: utf-8 -*-
"""
/***************************************************************************
 quickcrs
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
from qgis.core import *
from qgis.gui import QgsGenericProjectionSelector, QgsProjectionSelector
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from quickcrs_dialog import quickcrsDialog
import os.path

class quickcrs:
    def __init__(self, iface):
        self.dlg = quickcrsDialog()
        global selectedcrs
        s = QSettings()
        selectedcrs=s.value("quickcrs/crs", "")
        if selectedcrs=="":
            self.dlg.labelselectedcrs.setText("No CRS selected")
        else:
            self.dlg.labelselectedcrs.setText(selectedcrs)
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&QuickCRS')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'quickcrs')
        self.toolbar.setObjectName(u'quickcrs')
        # Create the dialog (after translation) and keep reference

        self.dlg.pushButton.clicked.connect(self.selectcrs)
        global isset
        self.dlg.button_box.accepted.connect(self.savesettings)

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('quickcrs', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=False,
        status_tip=None,
        whats_this=None,
        parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def add_action_toolbar(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=False,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        icon = QIcon(icon_path)
        actiontoolbar = QAction(icon, text, parent)
        actiontoolbar.triggered.connect(callback)
        actiontoolbar.setEnabled(enabled_flag)

        if status_tip is not None:
            actiontoolbar.setStatusTip(status_tip)

        if whats_this is not None:
            actiontoolbar.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(actiontoolbar)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                actiontoolbar)

        self.actions.append(actiontoolbar)

        return actiontoolbar

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = ':/plugins/quickcrs/icon.png'
        settings_icon_path = ':/plugins/quickcrs/settings.png'
        self.add_action_toolbar(
            icon_path,
            text=self.tr(u'Set Favourite CRS'),
            callback=self.run,
            parent=self.iface.mainWindow())
        self.add_action(
            icon_path,
            text=self.tr(u'Set Favourite CRS'),
            callback=self.run,
            parent=self.iface.mainWindow())
        self.add_action(
            settings_icon_path,
            text=self.tr(u'Settings for QuickCRS'),
            callback=self.settings,
            parent=self.iface.mainWindow())

    def settings(self):
        global isrun
        isrun="no"
        s = QSettings()
        selectedcrs=s.value("quickcrs/crs", "")
        if selectedcrs=="":
            self.dlg.labelselectedcrs.setText("No CRS selected")
        self.dlg.show()

    def savesettings(self):
        # print selectedcrs
        global isset
        if isset is None:
            isset="no"
        s = QSettings()
        s.setValue("quickcrs/crs", selectedcrs)
        if isset=="no" and isrun=="yes":
            self.updatecrs()

    def selectcrs(self):
        projSelector = QgsGenericProjectionSelector()
        projSelector.exec_()
        projSelector.selectedCrsId()
        #projSelector.selectedEpsg()
        global selectedcrs
        selectedcrs=projSelector.selectedAuthId()
        self.dlg.labelselectedcrs.setText(selectedcrs)
        self.dlg.show()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&QuickCRS'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def updatecrs(self):
        s = QSettings()
        selectedcrs=s.value("quickcrs/crs", "")
        # print selectedcrs
        canvas = self.iface.mapCanvas()
        if not canvas.hasCrsTransformEnabled():
            canvas.setCrsTransformEnabled(True)
        target_crs = QgsCoordinateReferenceSystem()
        target_crs.createFromUserInput(selectedcrs)
        canvas.setDestinationCrs(target_crs)
        canvas.freeze(False)
        canvas.setMapUnits(0)
        canvas.refresh()

    def run(self):
        """Run method that performs all the real work"""
        s = QSettings()
        selectedcrs=s.value("quickcrs/crs", "")
        global isset
        global isrun
        if selectedcrs=="":
            global isrun
            isrun="yes"
            isset="no"
            self.dlg.show()
        else:
            isset="yes"
            isrun="yes"
            self.updatecrs()
