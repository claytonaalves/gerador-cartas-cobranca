#coding: utf8
import sys
sys.path.insert(1, '..')

from collections import namedtuple
from cartas import CartasCobranca
from datetime import datetime, timedelta

def test():
    empresa = namedtuple('Empresa', 'idempresa, fantasia, endereco, cidade, telefone')
    empresa.idempresa = 1
    empresa.fantasia = 'Clayton Co'
    empresa.endereco = 'rua xxx, num. 1000, centro'
    empresa.cidade = 'Alta Floresta - MT'
    empresa.telefone = '3333-3333'

    titulos = []

    titulo = namedtuple('Titulo', 'numero, contrato, nome, endereco, bairro, uf, telefone, nossonumero, vencimento, valor, valor_com_juros, dias_atraso')
    titulo.numero = 1234
    titulo.contrato = str(titulo.numero).zfill(5)
    titulo.nome = 'Clayton de Almeida Alves'
    titulo.endereco = 'Rua das flores'
    titulo.bairro = 'Centro'
    titulo.cidade = 'Alta Floresta'
    titulo.uf = 'MT'
    titulo.telefone = '1234-4321'
    titulo.nossonumero = '00000000005-1'
    titulo.vencimento = datetime.now()
    titulo.valor = 42.42
    titulo.valor_com_juros = 42.42
    titulo.dias_atraso = 10
    titulos.append(titulo)

    titulo = namedtuple('Titulo', 'numero, contrato, nome, endereco, bairro, uf, telefone, nossonumero, vencimento, valor, valor_com_juros, dias_atraso')
    titulo.numero = 1234
    titulo.contrato = str(titulo.numero).zfill(5)
    titulo.nome = 'Clayton de Almeida Alves'
    titulo.endereco = 'Rua das flores'
    titulo.bairro = 'Centro'
    titulo.cidade = 'Alta Floresta'
    titulo.uf = 'MT'
    titulo.telefone = '1234-4321'
    titulo.nossonumero = '00000000003-1'
    titulo.vencimento = datetime.now()
    titulo.valor = 31.2
    titulo.valor_com_juros = 31.2
    titulo.dias_atraso = 10
    titulos.append(titulo)

    titulo = namedtuple('Titulo', 'numero, contrato, nome, endereco, bairro, uf, telefone, nossonumero, vencimento, valor, valor_com_juros, dias_atraso')
    titulo.numero = 2532
    titulo.contrato = str(titulo.numero).zfill(5)
    titulo.nome = u'Vanessa Andrade de Mendonça'
    titulo.endereco = u'Rua Dom João VI'
    titulo.bairro = 'Bom Pastor'
    titulo.cidade = 'Alta Floresta'
    titulo.uf = 'MT'
    titulo.telefone = '1234-4321'
    titulo.nossonumero = '00000000007-1'
    titulo.vencimento = datetime.now()
    titulo.valor = 23.5
    titulo.valor_com_juros = 23.5
    titulo.dias_atraso = 10
    titulos.append(titulo)

    titulo = namedtuple('Titulo', 'numero, contrato, nome, endereco, bairro, uf, telefone, nossonumero, vencimento, valor, valor_com_juros, dias_atraso')
    titulo.numero = 571
    titulo.contrato = str(titulo.numero).zfill(5)
    titulo.nome = u'Outro cliente'
    titulo.endereco = u'Rua Teste'
    titulo.bairro = 'Setor Novo'
    titulo.cidade = 'Alta Floresta'
    titulo.uf = 'MT'
    titulo.telefone = '1234-4321'
    titulo.nossonumero = '00000000093-1'
    titulo.vencimento = datetime.now()
    titulo.valor = 75
    titulo.valor_com_juros = 75
    titulo.dias_atraso = 10
    titulos.append(titulo)

    cartas = CartasCobranca()
    cartas.empresa = empresa
    cartas.template_path = '../../templates'
    cartas.template      = 'template1.html'
    cartas.taxa_religamento = 10.2
    cartas.pagar_ate = datetime.now()+timedelta(days=15)
    cartas.data_bloqueio = datetime.now()+timedelta(days=20)
    cartas.local_pagamento = 'ESCRITÓRIO GUSMÃO E CIA Parque Shopping – 2o piso – Centro – Cordeiro – RJ'
    cartas.gerar(titulos, '/tmp/testecarta.pdf')

if __name__=="__main__":
    test()


