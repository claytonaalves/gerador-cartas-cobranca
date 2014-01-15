#coding: utf8
import MySQLdb
import datetime
from string import Template
from pdb import set_trace
from pprint import pprint

IDEMPRESA = '1'
atraso = datetime.timedelta(days=15)
vcto_inicial = '1900-01-01'
vcto_final   = (datetime.datetime.now()-atraso).strftime('%Y-%m-%d')
taxa_religamento = '10,00'

# Rio Cable/Som Sat
conn = MySQLdb.connect('127.0.0.1', 'claytontemp', 'nonono', 'vigo')
q = conn.cursor()

# Obtém os dados da empresa
q.execute('select fantasia, cidade, uf, telefone from empresas where id=%s' % IDEMPRESA)

fantasia, cidade_emp, uf, telefone_empresa = q.fetchone()
cidade_emp = "%s - %s" % (cidade_emp, uf)

query = """\
select bol.nnumero, bol.vcto, bol.valor, bol.nome, bol.cidade, bol.endereco, t1.numero, t1.bairro, t1.telefone from 
	(select distinct
		u.numero,
		u.bairro,
		u.telefone
	from boletos b
	left join usuarios u using(numero)
	where 
		u.idempresa=%s and
		u.situacao='' and
		b.pago='0' and
		b.vcto between '%s' and '%s'
	order by u.nome) t1
left join boletos bol on t1.numero=bol.numero
where bol.pago='0' and bol.vcto<curdate()
order by nome, vcto
""" % (IDEMPRESA, vcto_inicial, vcto_final)

base = open('base.html', 'r')
base_template = base.read().decode('utf8')
base.close()

template = open('template.html', 'r').read().decode('utf8')

q.execute(query)

class Cliente:
    def __repr__(self):
        return u'%d -  %s' % (self.numero, repr(self.boletos))

clientes = {}

for nnumero, vcto, valor, nome, cidade, endereco, numero, bairro, telefone in q:
    vencimento = vcto.strftime('%d/%m/%Y')
    valor = str(valor).replace('.', ',')

    if numero in clientes:
        clientes[numero].boletos.append((nnumero, vencimento, valor))
        continue

    cliente = Cliente()
    cliente.numero = numero
    cliente.nnumero  = nnumero  
    cliente.vcto     = vcto     
    cliente.valor    = valor    
    cliente.nome     = nome.decode('latin1')
    cliente.cidade   = cidade.decode('latin1')
    cliente.endereco = endereco.decode('latin1') 
    cliente.bairro   = bairro.decode('latin1')
    cliente.telefone = telefone 
    cliente.boletos  = []
    cliente.boletos.append((nnumero, vencimento, valor))

    clientes[numero] = cliente


cartas = []
boletos_tpl = Template('<p class="mono">$nnumero $vencimento    $valor</p>')

for numero, cliente in clientes.iteritems():
    s = Template(template)

    boletos = []
    for boleto in cliente.boletos:
        #set_trace()
        boletos.append(boletos_tpl.substitute(
            nnumero    = boleto[0],
            vencimento = boleto[1],
            valor      = boleto[2]))

    

    fantasia = fantasia.decode('latin1')
    cidade   = cidade_emp.decode('latin1')
    nome_cliente = cliente.nome
    endereco = cliente.endereco

    saida = s.substitute(
        nome_empresa = fantasia,
        cidade       = cidade,
        data         = datetime.datetime.now().strftime('%d/%m/%Y'),
        nome_cliente = nome_cliente,
        contrato = str(cliente.numero).zfill(5),
        endereco = endereco,
        bairro = cliente.bairro,
        telefone = cliente.telefone,
        telefone_empresa=telefone_empresa,
        logofile='logo%s.jpg' % IDEMPRESA,
        taxa_religamento=taxa_religamento,
        lista_boletos=''.join(boletos))
    cartas.append(saida)

final = "".join(cartas)

output = base_template.replace('%{body}s', final)

f = open('output.html', 'w')
f.write(output.encode('utf8'))
f.close()
