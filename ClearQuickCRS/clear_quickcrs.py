# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ClearQuickCRS
                                 A QGIS plugin
 Clear QuickCRS settings
                              -------------------
        begin                : 2017-03-07
        git sha              : $Format:%H$
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

try:
    from qgis.PyQt.QtCore import QSettings
except ImportError:
    from PyQt4.QtCore import QSettings
try:
    from qgis.PyQt.QtGui import QIcon
    from qgis.PyQt.QtWidgets import QAction
except ImportError:
    from PyQt4.QtGui import QAction, QIcon
try:
    from .resources import *
except ImportError:
    from .resources3 import *
import os.path

class ClearQuickCRS:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ClearQuickCRS_{}.qm'.format(locale))

        # if os.path.exists(locale_path):
        #    self.translator = QTranslator()
        #    self.translator.load(locale_path)

        #    if qVersion() > '4.3.3':
        #        QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        #self.menu = self.tr(u'&ClearQuickCRS')
        self.menu = '&ClearQuickCRS'
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'ClearQuickCRS')
        self.toolbar.setObjectName(u'ClearQuickCRS')

    # noinspection PyMethodMayBeStatic
    #def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        # return QCoreApplication.translate('ClearQuickCRS', message)


    def add_action(
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

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ClearQuickCRS/icon.png'
        self.add_action(
            icon_path,
            #text=self.tr(u'Clear QuickCRS Settings'),
            text='Clear QuickCRS Settings',
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                #self.tr(u'&ClearQuickCRS'),
                u'&ClearQuickCRS',
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        s = QSettings()
        selectedcrs=s.remove("quickcrs/crs")
