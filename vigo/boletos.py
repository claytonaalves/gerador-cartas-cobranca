QUERY_BOLETOS_ATRASADOS = (
    "select                                                   "
    "    bol.nnumero,                                         "
    "    bol.vcto,                                            "
    "    datediff(curdate(), bol.vcto) as dias_atraso,        "
    "    bol.valor,                                           "
    "    cli.nome,                                            "
    "    cli.numero,                                          "
    "    lpad(cli.numero, 5, '0') as contrato,                "
    "    cli.cidade,                                          "
    "    cli.uf,                                              "
    "    cli.cep,                                             "
    "    cli.endereco,                                        "
    "    cli.bairro,                                          "
    "    cli.telefone                                         "
    "from boletos bol                                         "
    "left join usuarios cli on (bol.numero=cli.numero)        "
    "where                                                    "
    "    bol.pago='0' and                                     "
    "    (bol.vcto between '%s' and '%s') and                 "
    "    bol.idempresa=%d and                                 "
    "    cli.situacao in (%s)                                 "
    " %s                                                      "
    "order by bol.nome, bol.vcto                              "
)

class Titulo(object):

    def __str__(self):
        return "<Titulo %s - valor: %.2f vcto: %s>" % (self.nossonumero, self.valor, self.vencimento)

def atrasados(conn, idempresa, situacao, vcto1, vcto2, grupo):
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

    query = QUERY_BOLETOS_ATRASADOS % (vcto1.strftime('%Y-%m-%d'), vcto2.strftime('%Y-%m-%d'), idempresa, situacao, filtro)

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

