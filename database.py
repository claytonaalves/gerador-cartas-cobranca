#coding: utf8
import MySQLdb

conn = MySQLdb.connect('127.0.0.1', 'claytontemp', 'nonono', 'vigo')
cursor = conn.cursor()

class Titulo:
    pass

class Empresa:

    def __init__(self, idempresa):
        # Obtém os dados da empresa
        cursor.execute('select fantasia, cidade, uf, telefone from empresas where id=%s' % idempresa)

        fantasia, cidade_emp, uf, telefone_empresa = cursor.fetchone()
        cidade_emp = "%s - %s" % (cidade_emp, uf)

        self.idempresa = idempresa
        self.fantasia  = fantasia.decode('latin1')
        self.cidade    = cidade_emp.decode('latin1')
        self.uf        = uf
        self.telefone  = telefone_empresa

    def titulos_atrasados(self):
        idempresa = 1
        situacao  = "''"
        vcto1     = '2014-01-01'
        vcto2     = '2014-03-31'
        atraso1   = 10
        atraso2   = 150
        titulos1  = 2
        titulos2  = 5

        query = ( "select                                                                        "
                  "   bol.nnumero,                                                               "
                  "   bol.vcto,                                                                  "
                  "   bol.valor,                                                                 "
                  "   bol.nome,                                                                  "
                  "   t1.cidade,                                                                 "
                  "   t1.endereco,                                                               "
                  "   t1.numero,                                                                 "
                  "   t1.bairro,                                                                 "
                  "   t1.telefone                                                                "
                  "from boletos bol                                                              "
                  "left join                                                                     "
                  "    (   select                                                                "
                  "            u.numero,                                                         "
                  "            u.bairro,                                                         "
                  "            u.telefone,                                                       "
                  "            u.endereco,                                                       "
                  "            u.cidade,                                                         "
                  "            count(*) as titulos_abertos                                       "
                  "        from boletos b                                                        "
                  "        left join usuarios u using(numero)                                    "
                  "        where                                                                 "
                  "            u.idempresa=%(idempresa)d and                                     "
                  "            u.situacao in (%(situacao)s) and                                  "
                  "            b.pago='0' and                                                    "
                  "            b.vcto between '%(vcto1)s' and '%(vcto2)s'                        "
                  "        group by (u.numero)                                                   "
                  "        order by u.nome                                                       "
                  "    ) t1 on t1.numero=bol.numero                                              "
                  "where                                                                         "
                  "    bol.pago='0'                                                              "
                  "    and ((datediff(curdate(), bol.vcto)) between %(atraso1)d and %(atraso2)d) "
                  "    and (t1.titulos_abertos between %(titulos1)d and %(titulos2)d)            "
                  "order by bol.nome, bol.vcto                                                   " )
        query = query % (locals())

        cursor.execute(query)

        for record in cursor:
            nnumero, vcto, valor, nome, cidade, endereco, numero, bairro, telefone = record

            titulo          = Titulo()
            titulo.nnumero  = nnumero
            titulo.vcto     = vcto.strftime('%d/%m/%Y')
            titulo.valor    = str(valor).replace('.', ',')
            titulo.nome     = nome.decode('latin1')
            titulo.numero   = numero
            titulo.cidade   = cidade.decode('latin1')
            titulo.endereco = endereco.decode('latin1')
            titulo.bairro   = bairro.decode('latin1')
            titulo.telefone = telefone

            yield titulo

def test():
    empresa = Empresa(1)
    for r in empresa.titulos_atrasados():
        print r.numero, r.nome, r.nnumero

if __name__=='__main__':
    test()
