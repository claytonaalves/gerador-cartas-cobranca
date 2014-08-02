#coding: utf8
import os
import subprocess
from datetime import datetime, timedelta
import tempfile
from jinja2 import Environment, FileSystemLoader
from shutil import copyfile

class CartasCobranca:

    local_pagamento = 'Indefinido'

    def __init__(self, template_path=None, template=None):
        self.template_path = template_path
        self.template      = template

    def data_filter(self, value):
        return value.strftime('%d/%m/%Y')

    def money_filter(self, value):
        value = '%.2f' % value
        return value.replace('.', ',')

    def gerar(self, titulos, filename):
        """ Gera as cartas em um arquivo .html e depois o processa para obter o .pdf
        """
        env = Environment(loader=FileSystemLoader(self.template_path))
        env.filters['data'] = self.data_filter
        env.filters['money'] = self.money_filter
        self.template = env.get_template(self.template)

        saida = self.template.render(
            empresa          = self.empresa,
            titulos          = titulos,
            emissao          = datetime.now(),
            taxa_religamento = self.taxa_religamento,
            pagar_ate        = datetime.now()+timedelta(days = 15),
            data_bloqueio    = datetime.now()+timedelta(days = 20),
            local_pagamento  = self.local_pagamento
        )

        # create a temporary file to store the .html
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.html')
        f.write(saida.encode('utf8'))
        f.flush()

        # copy logo file
        copyfile('%s/logo_empresa_%d.jpg' % (self.template_path, self.empresa.idempresa), '/tmp/logo_empresa_%d.jpg' % self.empresa.idempresa)

        # generate .pdf file
        FNULL = open(os.devnull, 'w')
        retcode = subprocess.call(["wkhtmltopdf", "-q", f.name, filename], stdout=FNULL, stderr=FNULL)

        f.close()

