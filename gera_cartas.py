#coding: utf8
import datetime
from string import Template
from database import *
from collections import OrderedDict

TAXA_RELIGAMENTO = '10,00'

class Cliente:
    def __repr__(self):
        return u'%d -  %s' % (self.numero, repr(self.boletos))

def gerar(idempresa):
    empresa = Empresa(idempresa)

    base = open('base.html', 'r')
    base_template = base.read().decode('utf8')
    base.close()

    template = open('template.html', 'r').read().decode('utf8')

    clientes = OrderedDict()

    for titulo in empresa.titulos_atrasados():
        if titulo.numero in clientes:
            clientes[titulo.numero].boletos.append(titulo)
            continue

        cliente = Cliente()
        cliente.numero   = titulo.numero
        cliente.nnumero  = titulo.nnumero  
        cliente.vcto     = titulo.vcto     
        cliente.valor    = titulo.valor    
        cliente.nome     = titulo.nome
        cliente.cidade   = titulo.cidade
        cliente.endereco = titulo.endereco
        cliente.bairro   = titulo.bairro
        cliente.telefone = titulo.telefone 
        cliente.boletos  = []
        cliente.boletos.append(titulo)

        clientes[titulo.numero] = cliente

    cartas = []
    boletos_tpl = Template('<p class="mono">$nnumero $vencimento    $valor</p>')

    for numero, cliente in clientes.iteritems():
        s = Template(template)

        boletos = []
        for boleto in cliente.boletos:
            boletos.append(boletos_tpl.substitute(
                nnumero    = titulo.nnumero,
                vencimento = titulo.vcto,
                valor      = titulo.valor))

        print numero, cliente.nome

        saida = s.substitute(
            nome_empresa     = empresa.fantasia,
            cidade           = empresa.cidade,
            data             = datetime.datetime.now().strftime('%d/%m/%Y'),
            nome_cliente     = cliente.nome,
            contrato         = str(cliente.numero).zfill(5),
            endereco         = cliente.endereco,
            bairro           = cliente.bairro,
            telefone         = cliente.telefone,
            telefone_empresa = empresa.telefone,
            logofile         = 'logo_empresa_%s.jpg' % empresa.idempresa,
            taxa_religamento = TAXA_RELIGAMENTO,
            lista_boletos    = ''.join(boletos))
        cartas.append(saida)

    final = "".join(cartas)

    output = base_template.replace('%{body}s', final)

    f = open('output.html', 'w')
    f.write(output.encode('utf8'))
    f.close()

if __name__=='__main__':
    gerar(1)
