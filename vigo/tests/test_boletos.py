import sys
sys.path.insert(1, '../..')

import MySQLdb
import datetime
from vigo import boletos

def test():
    conn = MySQLdb.connect('localhost', 'testuser', '1234', 'vigo')
    titulos       = boletos.atrasados(conn,
        idempresa = 1,
        situacao  = "''",
        vcto1     = datetime.date(2014, 1, 1),
        vcto2     = datetime.date(2014, 8, 15),
    )

    for titulo in titulos:
        print titulo, titulo.contrato

if __name__=='__main__':
    test()


