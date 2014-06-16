""" This is a really dummy test to check if the script
    is generating the html and pdf correctly.
"""

import sys
import datetime
from collections import namedtuple

sys.path.append('../lib')
from cartas import CartasCobranca

empresa = namedtuple('Empresa', 'idempresa, fantasia, cidade, telefone')
cliente = namedtuple('Cliente', 'numero, nome, endereco, bairro, telefone, boletos')

empresa.idempresa = 1
empresa.fantasia = 'Clayton Co'
empresa.cidade = 'Alta Floresta - MT'
empresa.telefone = '3333-3333'
cartas = CartasCobranca(empresa)

# Cria um cliente com um titulo
cliente.numero = 1234
cliente.nome = 'Clayton de Almeida Alves'
cliente.endereco = 'Rua das flores'
cliente.bairro = 'Centro'
cliente.telefone = '1234-4321'
cliente.boletos = []

titulo = namedtuple('Titulo', 'nnumero, vencimento, valor')
titulo.nnumero = '00000000001-1'
titulo.vencimento = datetime.datetime.now()
titulo.valor = 42.42
cliente.boletos.append(titulo)
cartas.append(cliente)

# Cria um cliente com dois titulos
cliente.numero = 4321
cliente.nome = 'Vanessa A. Mendonca'
cliente.endereco = 'Rua das Oliveiras'
cliente.bairro = 'Bom Pastor'
cliente.telefone = '4321-4321'
cliente.boletos = []

titulo = namedtuple('Titulo', 'nnumero, vencimento, valor')
titulo.nnumero = '00000000002-1'
titulo.vencimento = datetime.datetime.now()
titulo.valor = 10.0
cliente.boletos.append(titulo)

titulo = namedtuple('Titulo', 'nnumero, vencimento, valor')
titulo.nnumero = '00000000003-1'
titulo.vencimento = datetime.datetime.now()+datetime.timedelta(days=1)
titulo.valor = 20
cliente.boletos.append(titulo)
cartas.append(cliente)


# Cria um cliente com quatro titulos
cliente.numero = 4321
cliente.nome = 'Cliente Devedor'
cliente.endereco = 'Rua das Bananeiras'
cliente.bairro = 'Testando'
cliente.telefone = '1111-1111'
cliente.boletos = []

titulo = namedtuple('Titulo', 'nnumero, vencimento, valor')
titulo.nnumero = '00000000004-1'
titulo.vencimento = datetime.datetime.now()
titulo.valor = 10.0
cliente.boletos.append(titulo)

titulo = namedtuple('Titulo', 'nnumero, vencimento, valor')
titulo.nnumero = '00000000005-1'
titulo.vencimento = datetime.datetime.now()+datetime.timedelta(days=1)
titulo.valor = 20
cliente.boletos.append(titulo)

titulo = namedtuple('Titulo', 'nnumero, vencimento, valor')
titulo.nnumero = '00000000006-1'
titulo.vencimento = datetime.datetime.now()+datetime.timedelta(days=2)
titulo.valor = 20
cliente.boletos.append(titulo)

titulo = namedtuple('Titulo', 'nnumero, vencimento, valor')
titulo.nnumero = '00000000007-1'
titulo.vencimento = datetime.datetime.now()+datetime.timedelta(days=3)
titulo.valor = 20
cliente.boletos.append(titulo)
cartas.append(cliente)

# Gera as cartas
cartas.gerar()


