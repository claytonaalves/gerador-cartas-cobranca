import sys
sys.path.insert(1, '../..')

import MySQLdb
from vigo import Empresa

def test():
    conn = MySQLdb.connect('localhost', 'testuser', '1234', 'vigo')
    empresa = Empresa(1, conn)
    print empresa

if __name__=='__main__':
    test()



