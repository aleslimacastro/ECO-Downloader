# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ECODownloader
                                 A QGIS plugin
 Esta ferramenta facilita a aquisição de dados hidrológicos disponíveis no Portal HidroWeb para a América do Sul.
                             -------------------
        begin                : 2017-06-02
        copyright            : (C) 2017 by Ingrid Petry, Daniel Gustavo Allasia Piccilli, Robson Leo Pachaly, Jessica Fontoura, Vitor Geller, Jean Favaretto.
        email                : ecoplugin@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ECODownloader class from file ECODownloader.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .eco_downloader import ECODownloader
    return ECODownloader(iface)
