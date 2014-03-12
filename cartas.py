import os
import subprocess
import datetime
import tempfile
from string import Template

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

TAXA_RELIGAMENTO = 1.1
PAGAR_ATE        = datetime.datetime.now()+datetime.timedelta(days=15)
DATA_BLOQUEIO    = datetime.datetime.now()+datetime.timedelta(days=20)

class CartasCobranca:

    def __init__(self, empresa):
        self.cartas = []
        self.empresa = empresa

    def append(self, cliente):
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
            taxa_religamento = TAXA_RELIGAMENTO,
            lista_boletos    = '\n'.join(titulos),
            pagar_ate        = PAGAR_ATE.strftime('%d/%m/%Y'),
            data_bloqueio    = DATA_BLOQUEIO.strftime('%d/%m/%Y'))
        self.cartas.append(saida)

    def gerar(self):
        """ Retornar nome do arquivo .pdf para iniciar download
        """
        base = open('%s/base.html' % dir_path, 'r')
        base_template = base.read().decode('utf8')
        base.close()

        final = "".join(self.cartas)

        output = base_template.replace('%{body}s', final)

        # create a temporary file to store the .html
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.html')
        f.write(output.encode('utf8'))
        f.flush()

        # generate .pdf file
        FNULL = open(os.devnull, 'w')
        retcode = subprocess.call(["wkhtmltopdf-amd64", "-q", f.name, "output.pdf"], stdout=FNULL, stderr=FNULL)

        f.close()

