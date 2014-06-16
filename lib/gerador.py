#coding: utf8
import datetime
from database import *
from cartas import CartasCobranca
from itertools import groupby
from collections import namedtuple

def gerar(idempresa, **kwargs):
    """ Gera um arquivo .pdf com as cartas de cobrança.
        Essa rotina espera os seguintes parâmetros:

        * situacao : pode ser "''", ou uma tupla ('', 'B', 'X')
        * vcto1    : vencimento inicial no formato Y-m-d
        * vcto2    : vencimento final também no formato Y-m-d
        * atraso1  : quantidade de dias em atraso (inteiro)
        * atraso2  : quantidade de dias em atraso (inteiro)
        * titulos1 : número de títulos em atraso (inteiro)
        * titulos2 : número de títulos em atraso (inteiro)
        * taxa_religamento
        * pagar_ate
        * data_bloqueio
    """
    empresa  = Empresa(idempresa)
    config = {
        'empresa': empresa,
        'taxa_religamento': kwargs['taxa_religamento'],
        'pagar_ate': kwargs['pagar_ate'],
        'data_bloqueio': kwargs['data_bloqueio']
    }
    cartas = CartasCobranca(config)

    # Um cliente pode ter 1 ou mais titulos em aberto...
    # Essa rotina eh responsavel por organizar os titulos, agrupando-os por cliente
    titulos = empresa.titulos_atrasados(**kwargs)

    for numero, cliente in groupby(titulos, lambda x: x.numero):
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

    cartas.gerar('novascartas.pdf')

def test():
    gerar( 
        1,
        situacao         = "''",
        vcto1            = '1900-01-01',
        vcto2            = '2014-05-10',
        atraso1          = 3,
        atraso2          = 150,
        titulos1         = 1,
        titulos2         = 5,
        taxa_religamento = 10.,
        #pagar_ate        = datetime.datetime.now()+datetime.timedelta(days = 15),
        #data_bloqueio    = datetime.datetime.now()+datetime.timedelta(days = 20)
        pagar_ate        = datetime.datetime(2014, 6, 2),
        data_bloqueio    = datetime.datetime(2014, 6, 3)
    )


if __name__=='__main__':
    test()

