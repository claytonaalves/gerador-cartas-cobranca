#coding: utf8
import sys
sys.path.append('./lib')

import os
import os.path
import MySQLdb
from bottle import route, run, template, request, static_file, redirect
from cartas import CartasCobranca
from vigo import boletos, Empresa
from datetime import datetime, timedelta

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)) 

DB_HOST     = os.environ.get('DB_HOST'     , 'localhost')
DB_USER     = os.environ.get('DB_USER'     , 'testuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD' , '1234')
DB_NAME     = os.environ.get('DB_NAME'     , 'vigo')

conn = MySQLdb.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, charset='latin1', use_unicode=True)

@route('/static/<filename:path>')
def static_files(filename):
    full_path = ROOT_PATH+'/static/'+filename
    root, filename = os.path.split(full_path)
    return static_file(filename, root=root)

#
# Responsavel por fazer a renderizacao da view principal
#
@route('/')
def main():
    conn.ping(True)
    cursor = conn.cursor()
    cursor.execute('select id, fantasia from empresas')
    taxa_religamento = "10,00"
    return template('index.html', empresas=cursor, taxa_religamento=taxa_religamento)


#
# Gera as cartas e retorna o link para download
#
@route('/cartas', method='POST')
def cartas():
    situacoes = {
        "ativos"      : "''",
        "bloqueados"  : "'B'",
        "desativados" : "'X'",
        "todos"       : "'', 'B', 'X'"
    }
    idempresa = int(request.forms.get('empresa'))
    empresa = Empresa(idempresa, conn)

    data_inicial   = request.forms.get('data_inicial')
    data_final     = request.forms.get('data_final')
    data_pagamento = request.forms.get('data_pagamento')
    data_corte     = request.forms.get('data_corte')

    if data_inicial=='' or data_final=='' or data_pagamento=='' or data_corte=='':
        redirect('/')

    titulos = boletos.atrasados(
        conn,
        idempresa = idempresa,
        situacao  = situacoes[request.forms.get('situacao')],
        vcto1     = datetime.strptime(data_inicial, '%d/%m/%Y'),
        vcto2     = datetime.strptime(data_final, '%d/%m/%Y'),
    )

    titulos = [titulo for titulo in titulos]
    if not titulos:
        redirect('semboletos')

    cartas = CartasCobranca()
    cartas.empresa = empresa
    cartas.template_path = 'templates'
    cartas.template      = 'template1.html'
    cartas.taxa_religamento = request.forms.get('taxa_religamento')
    cartas.pagar_ate = datetime.strptime(data_pagamento, '%d/%m/%Y')
    cartas.data_bloqueio = datetime.strptime(data_corte, '%d/%m/%Y')

    pdfname = 'cartas_cobranca_%s_a_%s' % (data_inicial.replace('/', '-'), data_final.replace('/', '-'))

    cartas.gerar(titulos, '%s/download/%s.pdf' % (ROOT_PATH, pdfname))

    redirect('download/%s.pdf' % pdfname)


@route('/semboletos')
def semboletos():
    return "Nao existem boletos nesta filtragem!"


@route('/download/<filename:path>')
def download(filename):
    full_path = ROOT_PATH+'/download/'+filename
    root, filename = os.path.split(full_path)
    return static_file(
               filename, 
               root=root
               #, download=True
           )          

run( host='0.0.0.0',
     port=8080,
     debug=True, 
     reloader=True 
 )
