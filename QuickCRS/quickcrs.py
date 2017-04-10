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
try:
    from qgis.gui import QgsGenericProjectionSelector
except ImportError:
    from qgis.gui import QgsProjectionSelectionDialog
try:
    from qgis.PyQt.QtCore import *
except ImportError:
    from PyQt4.QtCore import *
try:
    from qgis.PyQt.QtGui import *
    from qgis.PyQt.QtWidgets import QAction
except ImportError:
    from PyQt4.QtGui import *
try:
    from .resources import *
except ImportError:
    from .resources3 import *
from .quickcrs_dialog import quickcrsDialog
import os.path

class quickcrs:
    def __init__(self, iface):
        self.dlg = quickcrsDialog()
        global selectedcrs
        s = QSettings()
        selectedcrs=s.value("quickcrs/crs", 0)
        # Check if the CRS in the settings is an integer. In version prior to v0.3 of this plugin, the setting contained a text value instead of an integer.
        try:
            testsetting = selectedcrs+1
        except TypeError:
            s.setValue("quickcrs/crs", 0)
            selectedcrs=s.value("quickcrs/crs", 0)
        # If no CRS is set, run nocrsselected()
        if selectedcrs=="" or selectedcrs==0 or selectedcrs is None:
            self.nocrsselected()
        else:
            self.dlg.labelselectedcrs.setText(self.CrsId2AuthID(selectedcrs))
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&QuickCRS')
        self.toolbar = self.iface.addToolBar(u'quickcrs')
        self.toolbar.setObjectName(u'quickcrs')
        # Create the dialog (after translation) and keep reference
        self.dlg.pushButton.clicked.connect(self.selectcrs)
        self.dlg.button_box.accepted.connect(self.savesettings)

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        return QCoreApplication.translate('quickcrs', message)


    def add_action(
        # the action for the menu items
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
        # The action for the toolbar button
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
        # Add the toolbar button and the menu items
        icon_path = ':/plugins/QuickCRS/icon.png'
        settings_icon_path = ':/plugins/QuickCRS/settings.png'
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

    def savesettings(self):
        # Save the selected CRS
        try:
            isset
        except NameError:
            isset="no"
        s = QSettings()
        s.setValue("quickcrs/crs", selectedcrs)
        if selectedcrs=="" or selectedcrs==0 or selectedcrs is None:
            isset="no"
        if isset=="no" and isrun=="yes" and selectedcrs!="" and selectedcrs!=0:
            self.updatecrs()

    def selectcrs(self):
        # Select a new CRS
        s = QSettings()
        previousselectedcrs=s.value("quickcrs/crs", 0)
        if previousselectedcrs=="" or previousselectedcrs==0 or previousselectedcrs is None:
            self.nocrsselected()
        global selectedcrs
        try:
            projSelector = QgsGenericProjectionSelector()
            projSelector.exec_()
            projSelector.selectedCrsId()
            selectedcrs=projSelector.selectedCrsId()
        except:
            projSelector = QgsProjectionSelectionDialog()
            projSelector.exec_()
            selectedcrsdef = projSelector.crs()
            selectedcrs=selectedcrsdef.srsid()
        if (selectedcrs=="" or selectedcrs==0 or self.CrsId2AuthID(selectedcrs)=="" or selectedcrs is None):
             selectedcrs=previousselectedcrs
        if (selectedcrs=="" or selectedcrs==0 or self.CrsId2AuthID(selectedcrs)=="" or selectedcrs is None) and (previousselectedcrs=="" or previousselectedcrs==0 or previousselectedcrs is None):
            self.nocrsselected()
        else:
            self.dlg.labelselectedcrs.setText(self.CrsId2AuthID(selectedcrs))
        self.dlg.show()

    def updatecrs(self):
        # Set the CRS of the project to the CRS that is saved in the settings
        s = QSettings()
        selectedcrs=s.value("quickcrs/crs", 0)
        target_crs = QgsCoordinateReferenceSystem()
        target_crs.createFromId( selectedcrs, QgsCoordinateReferenceSystem.InternalCrsId )
        try:
            canvas = self.iface.mapCanvas()
            if not canvas.hasCrsTransformEnabled():
                canvas.setCrsTransformEnabled(True)
            canvas.setDestinationCrs(target_crs)
            canvas.freeze(False)
            canvas.setMapUnits(0)
            canvas.refresh()
        except:
            QgsProject.instance().setCrs(target_crs)


    def CrsId2AuthID(self, crsid=0):
        toconvert = QgsCoordinateReferenceSystem()
        if crsid=="" or crsid==0 or crsid is None:
            converted=""
        else:
            toconvert.createFromId(int(crsid), QgsCoordinateReferenceSystem.InternalCrsId)
            converted=toconvert.authid()
        return converted

    def nocrsselected(self):
        self.dlg.labelselectedcrs.setText("No CRS selected")

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&QuickCRS'),
                action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def settings(self):
        # Run the settings menu
        global isrun
        isrun="no"
        s = QSettings()
        selectedcrs=s.value("quickcrs/crs", 0)
        if selectedcrs=="" or selectedcrs==0 or selectedcrs is None:
            self.nocrsselected()
        self.dlg.show()

    def run(self):
        # Check wich part of the plugin must be run
        s = QSettings()
        selectedcrs=s.value("quickcrs/crs", 0)
        global isset
        global isrun
        if selectedcrs=="" or selectedcrs==0 or selectedcrs is None:
            isrun="yes"
            isset="no"
            self.nocrsselected()
            self.dlg.show()
        else:
            isset="yes"
            isrun="yes"
            self.updatecrs()
