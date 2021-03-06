#coding: utf8

class Empresa:

    _query_ = 'select fantasia, rsocial, endereco, cidade, uf, bairro, telefone from empresas where id=%s'

    def __init__(self, idempresa, conn):
        """ Obtém os dados da empresa

        :param idempresa: id da empresa de onde serao listados os titulos
        :param conn: conexao com o mysql
        """
        conn.ping(True)
        self.cursor = conn.cursor()

        self.cursor.execute(self._query_, (idempresa,))
        fantasia, razao, endereco, cidade, uf, bairro, telefone = self.cursor.fetchone()

        self.idempresa = idempresa
        self.razao     = razao
        self.fantasia  = fantasia
        self.endereco  = endereco
        self.cidade    = cidade
        self.uf        = uf
        self.bairro    = bairro
        self.telefone  = telefone

    def __str__(self):
        return "<Empresa %d: %s (%s - %s)>" % (self.idempresa, self.fantasia, self.cidade, self.uf)


