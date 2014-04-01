#coding: utf8
import os
import subprocess
import datetime
import tempfile
from string import Template

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

class CartasCobranca:

    def __init__(self, config):
        self.cartas = []
        self.config = config
        self.empresa = config['empresa']

    def append(self, cliente):
        """ Adiciona uma carta a coleção de cartas.
        """
        template = open('%s/template.html' % dir_path, 'r').read().decode('utf8')
        s = Template(template)

        boletos_tpl = Template('$nnumero  $vencimento  $valor')

        titulos = []
        for titulo in cliente.boletos:
            titulos.append(boletos_tpl.substitute(
                nnumero    = titulo.nnumero,
                vencimento = titulo.vencimento.strftime('%d/%m/%Y'),
                valor      = ("%.2f" % titulo.valor).replace('.', ',')))

        saida = s.substitute(
            nome_empresa     = self.empresa.fantasia,
            cidade           = self.empresa.cidade,
            data             = datetime.datetime.now().strftime('%d/%m/%Y'),
            nome_cliente     = cliente.nome,
            contrato         = str(cliente.numero).zfill(5),
            endereco         = cliente.endereco,
            bairro           = cliente.bairro,
            telefone         = cliente.telefone,
            telefone_empresa = self.empresa.telefone,
            logofile         = '%s/logo_empresa_%s.jpg' % (dir_path, self.empresa.idempresa),
            taxa_religamento = self.config['taxa_religamento'],
            lista_boletos    = '\n'.join(titulos),
            pagar_ate        = self.config['pagar_ate'].strftime('%d/%m/%Y'),
            data_bloqueio    = self.config['data_bloqueio'].strftime('%d/%m/%Y'))
        self.cartas.append(saida)

    def gerar(self):
        """ Gera as cartas em .html e depois as processa para obter o .pdf
            Retorna o nome do arquivo .pdf para iniciar download
        """
        base = open('%s/base.html' % dir_path, 'r')
        base_template = base.read().decode('utf8')
        base.close()

        final = "".join(self.cartas)

        output = base_template.replace('%{body}s', final)

        # create a temporary file to store the .html
        #f = tempfile.NamedTemporaryFile(mode='w', suffix='.html')
        f = open('output.html', 'w')
        f.write(output.encode('utf8'))
        f.flush()

        # generate .pdf file
        FNULL = open(os.devnull, 'w')
        retcode = subprocess.call(["wkhtmltopdf-amd64", "-q", f.name, "output.pdf"], stdout=FNULL, stderr=FNULL)

        # TODO: gravar o .pdf em um arquivo temporario e retornar o nome do arquivo

        f.close()

def test():
    from collections import namedtuple
    empresa = namedtuple('Empresa', 'idempresa, fantasia, cidade, telefone')
    cliente = namedtuple('Cliente', 'numero, nome, endereco, bairro, telefone, boletos')

    config = {
        'empresa'          : empresa,
        'taxa_religamento' : 10.2,
        'pagar_ate'        : datetime.datetime.now()+datetime.timedelta(days=15),
        'data_bloqueio'    : datetime.datetime.now()+datetime.timedelta(days=20)
    }

    empresa.idempresa = 1
    empresa.fantasia = 'Clayton Co'
    empresa.cidade = 'Alta Floresta - MT'
    empresa.telefone = '3333-3333'
    cartas = CartasCobranca(config)

    # Cria um cliente com um titulo
    cliente.numero = 1234
    cliente.nome = 'Clayton de Almeida Alves'
    cliente.endereco = 'Rua das flores'
    cliente.bairro = 'Centro'
    cliente.telefone = '1234-4321'
    cliente.boletos = []

    titulo = namedtuple('Titulo', 'nnumero, vencimento, valor')
    titulo.nnumero = '00000000001-1'
    titulo.vencimento = datetime.datetime.now()
    titulo.valor = 42.42
    cliente.boletos.append(titulo)
    cartas.append(cliente)

    cartas.gerar()

if __name__=="__main__":
    test()

