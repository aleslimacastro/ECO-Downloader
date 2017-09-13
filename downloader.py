# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import shutil
from PyQt4.QtGui import QProgressBar
from PyQt4.QtCore import *
import time


#### By Arthur modificado por Vitor Geller 
class Hidroweb(object):

    url_estacao = 'http://hidroweb.ana.gov.br/Estacao.asp?Codigo={0}&CriaArq=true&TipoArq={1}'
    url_arquivo = 'http://hidroweb.ana.gov.br/{0}'

    def __init__(self, estacoes, opcao, pathname, iface):
        self.estacoes = estacoes
        self.opcao = opcao
        self.pathname = pathname
        self.iface = iface

    def montar_url_estacao(self, estacao, tipo=1):
        return self.url_estacao.format(estacao, tipo)

    def montar_url_arquivo(self, caminho):
        return self.url_arquivo.format(caminho)

    def montar_nome_arquivo(self, estacao):
        
        return (self.pathname + '/{0}.zip'.format(estacao))

    def salvar_arquivo_texto(self, estacao, link):
        r = requests.get(self.montar_url_arquivo(link), stream=True)
        if r.status_code == 200:
            with open(self.montar_nome_arquivo(estacao), 'wb') as f:
            
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                
            print '** %s ** (Baixando)' % (estacao, )
        else:
            print '** %s ** (Problema)' % (estacao, )

    def obter_link_arquivo(self, response):
        soup = BeautifulSoup(response.content)
        return soup.find('a', href=re.compile('^ARQ/'))['href']

    def executar(self):
        
        progressMessageBar = self.iface.messageBar().createMessage(u'ECO Downloader', u' Baixando Dados... Isso poderá levar alguns minutos.')
        progress = QProgressBar()
        progress.setMaximum(len(self.estacoes))
        progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        progressMessageBar.layout().addWidget(progress)
        self.iface.messageBar().pushWidget(progressMessageBar, self.iface.messageBar().INFO)     
        
        opcao = self.opcao
        
        if opcao == 1:
            post_data = {'cboTipoReg': '10'} # para chuvas
            
        elif opcao == 2:
            post_data = {'cboTipoReg': '8'} # para cotas
            
        elif opcao == 3:
            post_data = {'cboTipoReg': '9'} # para vazões

        elif opcao == 4:
            post_data = {'cboTipoReg': '12'} # qualidade da água
            
        elif opcao == 5:
            post_data = {'cboTipoReg': '13'} # resumo de descarga
        
        elif opcao == 6:
            post_data = {'cboTipoReg': '16'} # perfil transversal
        
        
        contagem = 0
        for idx, est in enumerate(self.estacoes):

            time.sleep(1)
            progress.setValue(idx + 1)
            
            try:
                print '** %s ** - Procurando dados...' % (est, )                
                r = requests.post(self.montar_url_estacao(est), data=post_data)
                link = self.obter_link_arquivo(r)
                self.salvar_arquivo_texto(est, link)
                print u'** %s ** (Concluído)' % (est, )
                contagem += 1 
            except:
                print u'** %s ** - ERRO: Estacão não possui dados ou verifique sua conexão e tente novamente.\n' % (est, )
        
        contagem = str(contagem)
        nEstacoes = str(len(self.estacoes))
                   
        self.iface.messageBar().clearWidgets()
        self.iface.messageBar().pushInfo(u'ECO Downloader', contagem + u' das ' + nEstacoes + u' estações selecionadas foram baixadas com sucesso.') 
