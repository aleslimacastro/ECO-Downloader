# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ECODownloaderDialog
                                 A QGIS plugin
 Esta ferramenta facilita a aquisição de dados hidrológicos disponíveis no Portal HidroWeb para a América do Sul.
                             -------------------
        begin                : 2017-06-02
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Ingrid Petry, Daniel Gustavo Allasia Piccilli, Robson Leo Pachaly, Jessica Fontoura, Vitor Geller, Jean Favaretto.
        email                : ecoplugin@gmail.com
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

from PyQt4 import QtGui, uic, QtCore

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'eco_downloader_dialog_base.ui'))


class ECODownloaderDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ECODownloaderDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        QtGui.QDialog.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
