from itertools import groupby

QUERY_BOLETOS_ATRASADOS = (
    "SELECT                                                   "
    "    cli.numero,                                          "
    "    bol.nnumero,                                         "
    "    bol.vcto,                                            "
    "    DATEDIFF(CURDATE(), bol.vcto) AS dias_atraso,        "
    "    bol.valor,                                           "
    "    cli.nome,                                            "
    "    LPAD(cli.numero, 5, '0') AS contrato,                "
    "    cli.cidade,                                          "
    "    cli.uf,                                              "
    "    cli.cep,                                             "
    "    cli.endereco,                                        "
    "    cli.bairro,                                          "
    "    cli.telefone                                         "
    "FROM boletos bol                                         "
    "LEFT JOIN usuarios cli ON (bol.numero=cli.numero)        "
    "WHERE                                                    "
    "    bol.pago='0'                                         "
    #"    and (bol.vcto between '{0}' and '{1}')               "
    "    and bol.idempresa={0}                                "
    "    and cli.situacao in ({1})                            "
    " {2}                                                     "
    "ORDER BY bol.nome, bol.vcto                              "
)

class Titulo(object):

    def __str__(self):
        return "<Titulo %s - valor: %.2f vcto: %s idcliente: %s>" % (self.nossonumero, self.valor, self.vencimento, self.numero)

def atrasados(conn, idempresa, situacao, vcto1, vcto2, grupo, qtde_boletos_vencidos):
    """ Retorna um generator com a lista de titulos em atraso

    :param conn: conexao com o banco mysql
    :param idempresa: id da empresa
    :param situacao: situacao do cadastro do cliente (liberado ''; bloqueado 'B')
    :param vcto1: data inicial do vencimento
    :param vcto2: data final do vencimento
    """
    cursor = conn.cursor()
    filtro = ""
    if grupo!='todos':
        filtro = 'AND grupocliente=("%s")' % grupo

    query = QUERY_BOLETOS_ATRASADOS.format(
       idempresa, 
       situacao, 
       filtro,
    )

    cursor.execute(query)
    boletos = cursor.fetchall()

    q1 = int(qtde_boletos_vencidos[0])
    q2 = int(qtde_boletos_vencidos[1])

    for idcliente, group in groupby(boletos, lambda x: x[0]):
        titulos = [t for t in group]
        if not (q1 <= len(titulos) <= q2):
            continue

        for record in titulos:
            numero, nnumero, vencimento, dias_atraso, valor, nome, contrato, \
            cidade, uf, cep, endereco, bairro, telefone = record

            if not (vcto1 <= vencimento <= vcto2):
                continue

            titulo                 = Titulo()
            titulo.nossonumero     = nnumero
            titulo.vencimento      = vencimento
            titulo.dias_atraso     = dias_atraso
            titulo.valor           = valor
            titulo.valor_com_juros = valor
            titulo.nome            = nome
            titulo.numero          = numero
            titulo.contrato        = contrato
            titulo.cidade          = cidade
            titulo.uf              = uf
            titulo.cep             = cep
            titulo.endereco        = endereco
            titulo.bairro          = bairro
            titulo.telefone        = telefone

            yield titulo


if __name__=="__main__":
    from datetime import date
    import MySQLdb
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', db='vigo')
    vcto1 = date(2015, 1, 1)
    vcto2 = date(2015, 11, 15)
    situacao = "'', 'B', 'X'"
    idempresa = 2
    titulos = atrasados(conn, idempresa, situacao, vcto1, vcto2, 'todos', (1, 1))
    for titulo in titulos:
        print titulo

