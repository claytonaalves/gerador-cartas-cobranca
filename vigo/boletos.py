QUERY_BOLETOS_ATRASADOS = (
    "SELECT                                                   "
    "    bol.nnumero,                                         "
    "    bol.vcto,                                            "
    "    DATEDIFF(CURDATE(), bol.vcto) AS dias_atraso,        "
    "    bol.valor,                                           "
    "    cli.nome,                                            "
    "    cli.numero,                                          "
    "    LPAD(cli.numero, 5, '0') AS contrato,                "
    "    cli.cidade,                                          "
    "    cli.uf,                                              "
    "    cli.cep,                                             "
    "    cli.endereco,                                        "
    "    cli.bairro,                                          "
    "    cli.telefone                                         "
    "FROM boletos bol                                         "
    "LEFT JOIN (                                              "
    "    SELECT numero, COUNT(*) AS qtde                      "
    "    FROM boletos b2                                      "
    "    WHERE b2.pago='0' AND b2.vcto<CURDATE()              "
    "    AND (b2.vcto between '{0}' AND '{1}')                "
    "    GROUP BY 1                                           "
    ") t3 ON (t3.numero=bol.numero)                           "
    "LEFT JOIN usuarios cli ON (bol.numero=cli.numero)        "
    "WHERE                                                    "
    "    bol.pago='0'                                         "
    "    and (bol.vcto between '{2}' and '{3}')               "
    "    and bol.idempresa={4}                                "
    "    and cli.situacao in ({5})                            "
    "    and t3.qtde between {6} and {7}                      "
    " {8}                                                     "
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
       vcto1.strftime('%Y-%m-%d'), 
       vcto2.strftime('%Y-%m-%d'),
       vcto1.strftime('%Y-%m-%d'), 
       vcto2.strftime('%Y-%m-%d'),
       idempresa, 
       situacao, 
       qtde_boletos_vencidos[0],
       qtde_boletos_vencidos[1],
       filtro,
    )

    cursor.execute(query)

    for record in cursor:
        nnumero, vencimento, dias_atraso, valor, nome, numero, contrato, \
        cidade, uf, cep, endereco, bairro, telefone = record

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
    from datetime import datetime
    import MySQLdb
    conn = MySQLdb.connect('localhost', 'root', '', 'vigo')
    vcto1 = datetime(2015, 1, 1)
    vcto2 = datetime(2015, 8, 31)
    situacao = "'', 'B', 'X'"
    titulos = atrasados(conn, 1, situacao, vcto1, vcto2, 'todos', (1, 3))
    for titulo in titulos:
        print titulo

