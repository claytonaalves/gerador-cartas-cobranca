#coding: utf8
import sys
sys.path.append('./lib')

import os.path
import MySQLdb
from bottle import route, run, template, request, static_file, redirect
from cartas import CartasCobranca
from vigo import boletos, Empresa
from datetime import datetime, timedelta

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)) 

conn = MySQLdb.connect('localhost', 'root', '', 'vigo')

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
    cursor = conn.cursor()
    cursor.execute('select id, fantasia from empresas')
    return template('index.html', empresas=cursor)

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
    diasatraso1    = int(request.forms.get('diasatraso1'))
    diasatraso2    = int(request.forms.get('diasatraso2'))
    parcelaatraso1 = int(request.forms.get('parcelaatraso1'))
    parcelaatraso2 = int(request.forms.get('parcelaatraso2'))

    titulos = boletos.atrasados(conn,
        idempresa = idempresa,
        situacao  = situacoes[request.forms.get('situacao')],
        vcto1     = datetime.strptime(data_inicial, '%d/%m/%Y').strftime('%Y-%m-%d'),
        vcto2     = datetime.strptime(data_final, '%d/%m/%Y').strftime('%Y-%m-%d'),
        atraso1   = diasatraso1,
        atraso2   = diasatraso2,
        titulos1  = parcelaatraso1,
        titulos2  = parcelaatraso2,
        juros     = 0.21
    )

    cartas = CartasCobranca()
    cartas.empresa = empresa
    cartas.template_path = 'templates'
    cartas.template      = 'template1.html'
    cartas.taxa_religamento = 10.2
    cartas.pagar_ate = datetime.now()+timedelta(days=15)
    cartas.data_bloqueio = datetime.now()+timedelta(days=20)
    #cartas.local_pagamento = 'ESCRITÓRIO GUSMÃO E CIA Parque Shopping – 2o piso – Centro – Cordeiro – RJ'

    pdfname = 'cartas_cobranca_%s_a_%s' % (data_inicial.replace('/', '-'), data_final.replace('/', '-'))

    cartas.gerar(titulos, '%s/download/%s.pdf' % (ROOT_PATH, pdfname))

    redirect('/download/%s.pdf' % pdfname)

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
