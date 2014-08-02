import sys
sys.path.insert(1, '../..')

from dbconn import conn
from vigo import Empresa

def test():
    empresa = Empresa(1, conn)
    print empresa

if __name__=='__main__':
    test()



