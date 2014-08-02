import datetime

# Essa consulta retorna os boletos em abertos no banco de dados
# do sistema Vigo. Ela possui uma subquery porque foi a unica
# forma que encontrei de fazer a filtragem por quantidade de
# titulos em aberto.
QUERY_BOLETOS_ATRASADOS = (
    "select                                                                        "
    "    bol.nnumero,                                                              "
    "    bol.vcto,                                                                 "
    "    bol.valor,                                                                "
    "    bol.nome,                                                                 "
    "    usu.uf,                                                                   "
    "    usu.cep,                                                                  "
    "    t1.cidade,                                                                "
    "    t1.endereco,                                                              "
    "    t1.numero,                                                                "
    "    t1.bairro,                                                                "
    "    t1.telefone,                                                              "
    "    usu.dt_situacao                                                           "
    "from boletos bol                                                              "
    "left join usuarios usu on (bol.numero=usu.numero)                             "
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
    "order by bol.nome, bol.vcto                                                   "
)

class Titulo(object):

    def __str__(self):
        return "<Titulo %s - valor: %.2f vcto: %s>" % (self.nossonumero, self.valor, self.vencimento)

def atrasados(conn, **kwargs):
    """ Retorna um generator com a lista de titulos em atraso

    :param idempresa: id da empresa
    :param conn: conexao com o banco mysql
    :param situacao: situacao do cadastro do cliente (liberado ''; bloqueado 'B')
    :param vcto1: data inicial do vencimento
    :param vcto2: data final do vencimento
    :param atraso1: numero de dias em atraso
    :param atraso2: numero de dias em atraso
    :param titulos1: numero de titulos em atraso
    :param titulos2: numero de titulos em atraso
    """
    cursor = conn.cursor()
    query = QUERY_BOLETOS_ATRASADOS % (kwargs)

    cursor.execute(query)
    for record in cursor:
        nnumero, vencimento, valor, nome, uf, cep, cidade, endereco, numero, bairro, telefone, dt_situacao = record

        #atraso = (dt_situacao-vencimento).days
        #if atraso<0:
            #atraso = (datetime.date.today()-vencimento).days

        titulo                 = Titulo()
        titulo.nossonumero     = nnumero
        titulo.vencimento      = vencimento
        titulo.dias_atraso     = (datetime.date.today() - vencimento).days
        titulo.valor           = valor
        #titulo.valor_com_juros = ((.033 * atraso * valor) + (.02*valor)) + valor
        titulo.valor_com_juros = valor
        #print dt_situacao, atraso
        #(valor * kwargs['juros']) + valor
        titulo.nome            = nome.decode('latin1')
        titulo.numero          = numero
        titulo.contrato        = str(numero).zfill(5)
        titulo.cidade          = cidade.decode('latin1')
        titulo.uf              = uf
        titulo.cep             = cep
        titulo.endereco        = endereco.decode('latin1')
        titulo.bairro          = bairro.decode('latin1')
        titulo.telefone        = telefone

        yield titulo

