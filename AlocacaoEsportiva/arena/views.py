from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from .models import Funcionario,Endereco,Arena,Quadra,Cliente,Reserva,Pagamento
from django.contrib import messages
from django.shortcuts import redirect 
from hashlib import sha256
from django.contrib.auth import authenticate, login
from datetime import datetime 


def login(request):
	status = request.GET.get('status')
	return render(request,'login.html', {'status': status})

def cadastro(request):
	status = request.GET.get('status')
	return render(request,'cadastro.html', {'status': status})

def home(request):
	return HttpResponse("ola")

def validaCadastro(request):
	nome = request.POST.get("nome")
	telefone = request.POST.get("telefone")
	estado = request.POST.get("estado")
	cidade = request.POST.get("cidade")
	bairro = request.POST.get("bairro")
	rua = request.POST.get("rua")
	numero = request.POST.get("numero")
	complemento = request.POST.get("complemento")
	cpf = request.POST.get("cpf")
	email = request.POST.get("email")
	senha = request.POST.get("senha")

	pessoa = Funcionario.objects.filter(email = email)

	if len(nome.strip()) == 0 or len(email.strip()) == 0:
		return redirect('/arena/cadastro/?status=1') 

	if len(senha) < 8:
		return redirect('/arena/cadastro/?status=2')

	senha = sha256(senha.encode()).hexdigest()

	if pessoa.exists():
		messages.info(request, 'Email já existe')
		return redirect('/arena/cadastro/?status=3')

	try:
		endereco = Endereco(estado=estado,cidade=cidade,bairro=bairro,rua=rua,numero=numero,complemento=complemento)
		endereco.save()
		print(endereco)
		arena = Arena.objects.filter()[0]
		funcionario = Funcionario(admin=False,arena=arena,senha=senha,nome=nome,telefone=telefone,cpf=cpf,email=email,endereco=endereco.id)
		funcionario.save()
		return redirect('/arena/login/?status=0')
	except Exception as e:
		print("Ocorreu um erro:", e)
		return redirect('/arena/cadastro/?status=4')


	return HttpResponse(f"{nome} - {telefone} - {estado} - {cidade} - {bairro} - {rua} - {numero} - {complemento} - {cpf} - {email} - {senha}")

def validaLogin(request):

    email = request.POST.get("email")
    senha = request.POST.get("senha")
    senha = sha256(senha.encode()).hexdigest()

    funcionario = Funcionario.objects.filter(email=email).filter(senha=senha)

    if len(funcionario) == 0:
        retorno = redirect('/arena/login/?status=1')
    else:
        request.session['funcionario'] = Funcionario.objects.filter(email=email)[0].id
        retorno = redirect(f'/arena/home/')

    return retorno


# Fazer um decorator para verificar se o usuário está autenticado

def autenticado(funcao):
	def wrapper(request, *args, **kwargs):
		user = request.session.get('funcionario')
		if user == None:
			retorno = redirect(f'/arena/login/')
		else:
			funcionario = Funcionario.objects.filter(id=user)[0]
			retorno = funcao(request, funcionario=funcionario, *args, **kwargs)
		return retorno
	return wrapper

@autenticado
def home(request, funcionario: Funcionario=None):
	return render(request,'home.html', {'nome': funcionario.nome})


def sair(request):
	request.session["funcionario"] = None
	return redirect('/arena/login/')

@autenticado
def verEspaco(request, funcionario:Funcionario=None):
	quadras = list(Quadra.objects.all())
	listaQuadra = [
        {'tipo': quadra.tipo, 'preco': quadra.preco} 
        for quadra in quadras
    ]
	return render(request,'verEspaco.html', {
		'nome': funcionario.nome,
		'qnt': len(quadras),
		'quadras': listaQuadra
		}
	)

@autenticado
def cadastrarEspaco(request, funcionario:Funcionario=None):
	status = request.GET.get('status')
	return render(request,'cadastrarEspaco.html', {
		'nome': funcionario.nome,
		'status': status
		})

@autenticado
def validaCadastrarEspaco(request, funcionario:Funcionario=None):
	tipo = request.POST.get("tipo")
	valor = request.POST.get("valor")

	if tipo == " ": 
		return redirect(f'/arena/cadastrarEspaco/?status = 1')
	else:
		quadra = Quadra(tipo=tipo,preco=float(valor),reservado = False)
		quadra.save()
	return redirect(f'/arena/home/?status = 0')


@autenticado
def verCliente(request, funcionario:Funcionario=None):
	clientes = list(Cliente.objects.all())
	listaCliente = [
        {'id': cliente.id,'nome': cliente.nome} 
        for cliente in clientes
    ]
	return render(request,'verCliente.html', {
		'nome': funcionario.nome,
		'qnt': len(clientes),
		'clientes': listaCliente
		}
	)

 



@autenticado
def cadastrarCliente(request, funcionario:Funcionario=None):
	return render(request,'cadastrarCliente.html', {'nome': funcionario.nome})


@autenticado
def validaCadastrarCliente(request, funcionario:Funcionario=None):
	nome = request.POST.get("nome")
	telefone = request.POST.get("telefone")
	estado = request.POST.get("estado")
	cidade = request.POST.get("cidade")
	bairro = request.POST.get("bairro")
	rua = request.POST.get("rua")
	numero = request.POST.get("numero")
	complemento = request.POST.get("complemento")
	cpf = request.POST.get("cpf")
	email = request.POST.get("email")

	pessoa = Cliente.objects.filter(email=email)

	if nome == " ": 
		return redirect(f'/arena/cadastrarCliente/?status = 1')
	else:
		endereco = Endereco(estado=estado,cidade=cidade,bairro=bairro,rua=rua,numero=numero,complemento=complemento)
		endereco.save()
		cliente = Cliente(nome=nome,telefone=telefone,cpf=cpf,email=email,endereco=endereco.id)
		cliente.save()
	return redirect(f'/arena/home/?status = 0')

@autenticado
def cliente(request,id,funcionario:Funcionario=None):
	cliente = Cliente.objects.get(id=id)
	endereco = Endereco.objects.get(id=cliente.endereco)
	return render(request,'cliente.html', {
		'cliente': cliente,
		'endereco': endereco
		})

@autenticado
def excluirCliente(request,id,funcionario:Funcionario=None):
	cliente = Cliente.objects.get(id=id)
	cliente.delete()
	return redirect(f"/arena/verCliente")



@autenticado
def validaEditarCliente(request,id):
	cliente = Cliente.objects.get(id=id)
    
	if request.method == 'POST':
		cliente.nome = request.POST.get('nome')
		cliente.telefone = request.POST.get('telefone')
		cliente.estado = request.POST.get('estado')
		cliente.cidade = request.POST.get('cidade')
		cliente.bairro = request.POST.get('bairro')
		cliente.rua = request.POST.get('rua')
		cliente.numero = request.POST.get('numero')
		cliente.complemento = request.POST.get('complemento')
		cliente.cpf = request.POST.get('cpf')
		cliente.email = request.POST.get('email')
		cliente.save()
		return redirect('verCliente',id=id)

	return render(request, 'editarCliente.html', {'cliente': cliente})

@autenticado
def editarCliente(request,id,funcionario:Funcionario=None):
    cliente = Cliente.objects.get(id=id)
    return render(request, 'editarCliente.html', {'cliente': cliente})


@autenticado
def verReservas(request, funcionario:Funcionario=None):
	reservas = list(Reserva.objects.all())
	listaReserva = [
        reserva for reserva in reservas
    ]
	return render(request,'verReservas.html', {
		'nome': funcionario.nome,
		'qnt': len(reservas),
		'reservas': listaReserva
		}
	)

@autenticado
def cadastrarReserva(request, funcionario:Funcionario=None):
	clientes = list(Cliente.objects.filter())
	quadras = list(Quadra.objects.filter())
	return render(request,'cadastrarReserva.html', {
			'nome': funcionario.nome,
			'clientes': clientes,
			'quadras': quadras

		})


def reservasSobrepostas(horaEntrada:datetime, horaSaida:datetime, tipo:str) -> bool:

	horaEntradaNova = horaEntrada
	horaSaidaNova = horaSaida
	reservasExistentes = Reserva.objects.filter(quadra=tipo)
    
	for reservaExistente in reservasExistentes:
		print(reservaExistente.horaSaida, type(reservaExistente.horaSaida))
		if (
			horaEntradaNova <= reservaExistente.horaSaida
			or reservaExistente.horaEntrada <= horaSaidaNova
		):
			return True # Choca horários de reserva

	return False # Não choca horários

def converteHorarios(hora:str) -> datetime:
	dataStr, horaStr = hora.split("T")
	nova = f"{dataStr} {horaStr}"
	dataNova = datetime.strptime(nova, '%Y-%m-%d %H:%M')
	return dataNova  # Imprime o objeto datetime convertido


@autenticado
def validaCadastrarReserva(request, funcionario:Funcionario=None):
	horaEntrada = request.POST.get("horaEntrada")
	horaSaida = request.POST.get("horaSaida")
	valor = request.POST.get("valor")
	cliente = request.POST.get("cliente")
	tipo = request.POST.get("tipo")
	status = request.POST.get("status")


	print(horaEntrada, horaSaida)

	horaEntradaObj = converteHorarios(horaEntrada)
	horaSaidaObj = converteHorarios(horaSaida)
     
	#choque = reservasSobrepostas(horaEntrada=horaEntradaObj, horaSaida=horaSaidaObj, tipo=tipo)

	clienteBuscado = Cliente.objects.filter(id=int(cliente))[0]
	quadraBuscada = Quadra.objects.filter(id=int(tipo))[0]
	reserva = Reserva(horaEntrada=horaEntradaObj,
		horaSaida=horaSaidaObj,
		valor=float(valor),
		cliente= clienteBuscado,
		quadra= quadraBuscada)
	reserva.save()
	return redirect(f"/arena/home/?status=0")


@autenticado
def reserva(request,id,funcionario:Funcionario=None):
	reserva = Reserva.objects.get(id=id)
	return render(request,'reserva.html', {
		'reserva': reserva
		})

@autenticado
def excluirReserva(request,id,funcionario:Funcionario=None):
	reserva = Reserva.objects.get(id=id)
	reserva.delete()
	return redirect(f"/arena/verReservas")



@autenticado
def validaEditarReserva(request,id, funcionario:Funcionario=None):
    reserva = Reserva.objects.get(id=id)
    if request.method == 'POST':
        valor = request.POST.get('valor')
        tipo_quadra = request.POST.get('tipo_quadra')
        horaEntrada = request.POST.get('horaEntrada')
        horaSaida = request.POST.get('horaSaida')

        reserva.valor = valor
        reserva.quadra = Quadra.objects.get(id=tipo_quadra)
        reserva.horaEntrada = datetime.strptime(horaEntrada, '%Y-%m-%dT%H:%M')
        reserva.horaSaida = datetime.strptime(horaSaida, '%Y-%m-%dT%H:%M')
        reserva.save()

        return redirect('verReservas')

    return render(request, 'editarReserva.html', {
        'reserva': reserva,
        'quadras': Quadra.objects.all(),
        'funcionario': funcionario
    })

@autenticado
def editarReserva(request, id, funcionario:Funcionario=None):
    reserva = Reserva.objects.get(id=id)
    quadras = Quadra.objects.all()
    return render(request, 'editarReserva.html', {
        'reserva': reserva,
        'quadras': quadras,
        'funcionario': funcionario
    })



@autenticado
def verPagamentos(request, funcionario:Funcionario=None):
	pagamentos = list(Pagamento.objects.all())

	return render(request,'verPagamento.html', {
		'qnt': len(pagamentos),
		'pagamentos': pagamentos
		}
	)

@autenticado
def cadastrarPagamento(request, funcionario:Funcionario=None):
	# Filtra as reservas que ainda não foram pagas
	reservasNaoPagas = Reserva.objects.exclude(pagamento__isnull=False)
	formas = ['Dinheiro', 'Pix', 'Cartao']


	return render(request,'cadastrarPagamento.html', {
			'formas': formas,
			'reservas': reservasNaoPagas
			#'reservas': reservas

		})


@autenticado
def validaCadastrarPagamento(request, funcionario:Funcionario=None):
	forma = request.POST.get("forma")
	data = request.POST.get("data")
	reserva = request.POST.get("reserva")

	reservaBuscado = Reserva.objects.get(id=reserva)

	pagamento = Pagamento(forma=forma,data=data,reserva=reservaBuscado)
	pagamento.save()
	return redirect(f"/arena/home/?status=0")

