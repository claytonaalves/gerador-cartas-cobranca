#coding: utf8
from database import *
from collections import OrderedDict
from cartas import CartasCobranca
from itertools import groupby
from collections import namedtuple

def gerar(idempresa):
    empresa  = Empresa(idempresa)
    cartas = CartasCobranca(empresa)

    # Um cliente pode ter 1 ou mais titulo em aberto...
    # Essa rotina eh responsavel por organizar os titulos, agrupando-os por cliente
    for numero, cliente in groupby(empresa.titulos_atrasados(), lambda x: x.numero):
        boletos  = []
        for titulo in cliente:
            boleto            = namedtuple('Boleto', 'nnumero, vencimento, valor')
            boleto.nnumero    = titulo.nnumero
            boleto.vencimento = titulo.vcto
            boleto.valor      = titulo.valor
            boletos.append(boleto)

        cliente          = namedtuple('Cliente', 'numero, nome, endereco, bairro, telefone, boletos')
        cliente.numero   = titulo.numero
        cliente.nome     = titulo.nome
        cliente.endereco = titulo.endereco
        cliente.bairro   = titulo.bairro
        cliente.telefone = titulo.telefone
        cliente.boletos  = boletos
        cartas.append(cliente)

    cartas.gerar()


if __name__=='__main__':
    gerar(1)

