import sys
sys.path.append('./lib')
import os
import os.path
from bottle import route, run, template, request, static_file
from database import cursor
import json

ROOT_PATH = os.path.dirname(os.path.abspath(__file__)) 

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
    cursor.execute('select id, fantasia from empresas')
    return template('index.html', empresas=cursor)

#
# Gera as cartas
#
@route('/cartas', method='POST')
def cartas():
    idempresa      = request.forms.get('empresa')
    situacao       = request.forms.get('situacao')
    diasatraso1    = request.forms.get('diasatraso1')
    diasatraso2    = request.forms.get('diasatraso2')
    parcelaatraso1 = request.forms.get('parcelaatraso1')
    parcelaatraso2 = request.forms.get('parcelaatraso2')
    data_inicial   = request.forms.get('data_inicial')
    data_final     = request.forms.get('data_final')
    return json.dumps(locals())

#@route('/download/<filename:path>')
#def download(filename):
#    return static_file(filename, root='/path/to/static/files', download=True)


run( host='0.0.0.0',
     port=8080,
     debug=True, 
     reloader=True 
 )
