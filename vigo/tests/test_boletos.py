import sys
sys.path.insert(1, '../..')

from dbconn import conn
from vigo import boletos

def test():
    titulos       = boletos.atrasados(conn,
        idempresa = 1,
        situacao  = "'B'",
        vcto1     = '2014-01-01',
        vcto2     = '2014-07-31',
        atraso1   = 10,
        atraso2   = 150,
        titulos1  = 1,
        titulos2  = 5,
        juros     = 0.21
    )

    for titulo in titulos:
        print titulo, titulo.dias_atraso, titulo.valor_com_juros

if __name__=='__main__':
    test()


