# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ECODownloader
                                 A QGIS plugin
 Esta ferramenta facilita a aquisição de dados hidrológicos disponíveis no Portal HidroWeb para a América do Sul.
                              -------------------
        begin                : 2016-01-25
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Ingrid Petry, Daniel Gustavo Allasia Piccilli, Robson Leo Pachaly, Jessica Fontoura, Vitor Geller, Jean Favaretto.
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QFileDialog
from PyQt4 import QtGui
from qgis.core import QgsVectorLayer, QgsMapLayerRegistry
from qgis.gui import QgsMessageBar
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from eco_downloader_dialog import ECODownloaderDialog
from qgis.utils import *
import os
import os.path
import qgis
from downloader import Hidroweb

class ECODownloader:
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
            'ECODownloader_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
            

        # Create the dialog (after translation) and keep reference
        self.dlg = ECODownloaderDialog()
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&ECO-Downloader')
        
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'ECODownloader')
        self.toolbar.setObjectName(u'ECODownloader')
        
        #Diretório para download de dados
        self.dlg.lineEdit.clear()
        self.dlg.pushButton.clicked.connect(self.select_output_file)
        

        #Pega o clique do botão fechar e conecta a função fechar
        self.dlg.fechar.clicked.connect(self.fechar)
        self.dlg.okay.clicked.connect(self.run)

        #Se mudar o índice do comboBox, conecta ao shapefile
        self.dlg.comboBox.currentIndexChanged.connect(self.insertMap)
        
    
       
    def insertMap(self):
        indice = self.dlg.comboBox.currentIndex()
        pluvio = "pluvio"
        fluvio = "fluvio"
                    
        if indice == 0:
            
            self.removeLayer()
            
        elif indice == 1:
            self.removeLayer()
            self.addLayer(pluvio)
                    
        elif indice >= 2 and indice <= 6: 
            self.removeLayer()
            self.addLayer(fluvio)
                       
    def addLayer(self, tipo):
        pluginpath = self.getCam()
        shape = QgsVectorLayer(pluginpath + "\\" + tipo, tipo,"ogr")
        QgsMapLayerRegistry.instance().addMapLayer(shape)
            
        
    def removeLayer(self):
        layerMap = QgsMapLayerRegistry.instance().mapLayers()
        
        for name, layer in layerMap.iteritems():
            if "pluvio" == str(layer.name()):
                registry = QgsMapLayerRegistry.instance()
                layerPluvio = registry.mapLayersByName("pluvio")[0]
                QgsMapLayerRegistry.instance().removeMapLayer(layerPluvio)
                
            elif "fluvio" == str(layer.name()):
                registry = QgsMapLayerRegistry.instance()
                layerFluvio = registry.mapLayersByName("fluvio")[0]
                QgsMapLayerRegistry.instance().removeMapLayer(layerFluvio)
                  
    def verifyLayer(self):
        layerMap = QgsMapLayerRegistry.instance().mapLayers()
        
        for name, layer in layerMap.iteritems():
            if "pluvio" == str(layer.name()):
                registry = QgsMapLayerRegistry.instance()
                layerPluvio = registry.mapLayersByName("pluvio")[0]
                return layerPluvio
                
            elif "fluvio" == str(layer.name()):
                registry = QgsMapLayerRegistry.instance()
                layerFluvio = registry.mapLayersByName("fluvio")[0]
                return layerFluvio
        
        #Função de buscar o caminho do plugin
    def getCam(self):
        plugin_path = os.path.dirname(os.path.realpath(__file__))
        return plugin_path
    
      #Seleciona o diretório de saída
    def select_output_file(self):
        filename = QFileDialog.getExistingDirectory(self.dlg, u'Selecione uma pasta de saída ',"C:\\", QtGui.QFileDialog.ShowDirsOnly)
        self.dlg.lineEdit.setText(filename)
    
    
    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ECODownloader', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

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

        icon_path = ':/plugins/ECODownloader/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'ECO-Downloader'),
            callback=self.inicio,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&ECO-Downloader'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
        
    
        #Função para fechar a janela do plugin    
    def fechar(self):
        self.dlg.close()
        
        #Função de abertura da janela do plugin
    def inicio(self):
        
        #Abre o Python Console quando inicia o plugin
        qgis.utils.iface.actionShowPythonDialog().trigger()
        
        #Limpa a comboBox para não repetir a lista
        self.dlg.comboBox.clear()
        
 
        #Inserção das opções de download na comboBox
        Lista = [" ", "Chuva","Cota",u"Vazão", u"Qualidade da Água", "Resumo de descarga", "Perfil transversal"]

        self.dlg.comboBox.addItems(Lista)
        
        self.removeLayer()
        self.dlg.show()
    
        
    
                                    
 #====================================================================================      
         
    def run(self):
        """Run method that performs all the real work"""
        diretorio = self.dlg.lineEdit.text()
        filename = diretorio + '\estacoes.txt'
        indice = self.dlg.comboBox.currentIndex() 
        if indice == 0:
            self.iface.messageBar().pushMessage("ERRO", u"Escolha a opção de download!", level=QgsMessageBar.CRITICAL)
            return None
        elif filename == '\estacoes.txt':
            self.iface.messageBar().pushMessage("ERRO", u"Indique um diretório para download dos dados!", level=QgsMessageBar.CRITICAL)
            return None
        else:
       
            output_file = open(filename, 'w')
            self.pathname = os.path.dirname(filename) #define o diretorio onde os arquivos serao baixados. Salva no mesmo diretorio do arquivo de texto
            
            
            selectedLayer = self.verifyLayer()
            selected_features = selectedLayer.selectedFeatures()
            
            valores =[]
        
            for f in selected_features:
                #selected_features = selectedLayer.selectedFeatures
                line = '%d' % (f['Codigo']) #%i
                lista = '%d\n' % (f['Codigo'])
                valores.append(line)
                output_file.write(lista)
            output_file.close()
            opcao = self.dlg.comboBox.currentIndex() #armazena o indice da opção de download
            self.rodarHidroWeb(valores, opcao) #rodar funcao "rodarHidroWeb"
            
    def rodarHidroWeb(self,valores, opcao): #chama a claase Hidroweb atribuindo as variaveis obtidas anteriormente
        
        hid = Hidroweb(valores, opcao, self.pathname, self.iface)
        hid.executar()  