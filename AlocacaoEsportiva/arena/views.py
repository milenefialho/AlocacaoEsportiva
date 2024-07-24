from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
import pytz
from .models import Funcionario,Endereco,Arena,Quadra,Cliente,Reserva,Pagamento
from django.contrib import messages
from django.shortcuts import redirect 
from hashlib import sha256
from django.contrib.auth import authenticate, login
from datetime import datetime 
from django.utils import timezone

def login(request):
	status = request.GET.get('status')
	return render(request,'login.html', {'status': status})

def cadastro(request):
	status = request.GET.get('status')
	return render(request,'cadastro.html', {'status': status})

# def home(request):
# 	return HttpResponse("ola")

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

	print('PASSOU AQUI!!!!!')

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
	return render(request,'home.html', {'funcionario': funcionario})


def sair(request):
	request.session["funcionario"] = None
	return redirect('/arena/login/')

@autenticado
def verEspaco(request,funcionario:Funcionario=None):
	quadras = list(Quadra.objects.all())
	listaQuadra = [
		{'id': quadra.id,'tipo': quadra.tipo, 'preco': quadra.preco} 
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
def espaco(request,id,funcionario:Funcionario=None):
	quadra = Quadra.objects.get(id=id)
	return render(request,'espaco.html', {
		'quadra': quadra
		})

@autenticado
def excluirEspaco(request,id,funcionario:Funcionario=None):
	quadra = Quadra.objects.get(id=id)
	quadra.delete()
	return redirect(f"/arena/verEspaco")


@autenticado
def validaEditarEspaco(request,id, funcionario:Funcionario=None):
	quadra = Quadra.objects.get(id=id)
	
	if request.method == 'POST':
		quadra.tipo = request.POST.get('tipo')
		quadra.preco = request.POST.get('preco')
		quadra.save()
		return redirect('espaco',id=id)

	return render(request, 'editarEspaco.html', {'quadra': quadra})

@autenticado
def editarEspaco(request, id, funcionario:Funcionario=None):
	quadra = Quadra.objects.get(id=id)
	return render(request, 'editarEspaco.html', {
		'quadra': quadra,
		'funcionario': funcionario
	})


@autenticado
def verCliente(request,funcionario:Funcionario=None):
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
def validaCadastrarCliente(request,funcionario:Funcionario=None):
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
def validaEditarCliente(request,id,funcionario:Funcionario=None):
	cliente = Cliente.objects.get(id=id)
	endereco = Endereco.objects.get(id=cliente.endereco)
	
	if request.method == 'POST':
		cliente.nome = request.POST.get('nome')
		cliente.telefone = request.POST.get('telefone')
		cliente.cpf = request.POST.get('cpf')
		cliente.email = request.POST.get('email')
		cliente.save()

		endereco.estado = request.POST.get('estado')
		endereco.cidade = request.POST.get('cidade')
		endereco.bairro = request.POST.get('bairro')
		endereco.rua = request.POST.get('rua')
		endereco.numero = request.POST.get('numero')
		endereco.complemento = request.POST.get('complemento')
		endereco.save()

	return redirect('verCliente')


@autenticado
def editarCliente(request,id,funcionario:Funcionario=None):
	cliente = Cliente.objects.get(id=id)
	endereco = Endereco.objects.get(id=cliente.endereco)
	return render(request, 'editarCliente.html', {'cliente': cliente,'endereco': endereco})


@autenticado
def verReservas(request, funcionario:Funcionario=None):
	status = request.GET.get('status')
	reservas = Reserva.objects.all()
	reservas = sorted(reservas, key=lambda x: x.horaEntrada, reverse=True)
	return render(request,'verReservas.html', {
		'nome': funcionario.nome,
		'qnt': len(reservas),
		'reservas': reservas,
		'status': status,
		'datas': None
		}
	)

@autenticado
def reservasFiltro(request, funcionario:Funcionario=None):
	status = request.GET.get('status')
	inicio = request.POST.get('inicial')
	fim = request.POST.get('final')
	inicio = timezone.datetime.strptime(inicio, '%Y-%m-%d')
	fim = timezone.datetime.strptime(fim, '%Y-%m-%d')
	# inicio = 23/07/2024 00:00:00
	# fim = 23/07/2024 23:59:59
	fim = fim.replace(hour=23, minute=59, second=59)
	
	reservas = Reserva.objects.filter(horaEntrada__range=[inicio, fim])
	reservas = sorted(reservas, key=lambda x: x.horaEntrada, reverse=True)
	return render(request,'verReservas.html', {
			'nome': funcionario.nome,
			'qnt': len(reservas),
			'reservas': reservas,
			'status': status,
			'datas': {
				'inicio': inicio,
				'fim': fim
			}
		}
	)

@autenticado
def cadastrarReserva(request, funcionario:Funcionario=None):
	clientes = list(Cliente.objects.all())
	quadras = list(Quadra.objects.all())
	return render(request,'cadastrarReserva.html', {
			'nome': funcionario.nome,
			'clientes': clientes,
			'quadras': quadras
		})

def ajustarData(data, formato: str = '%Y-%m-%dT%H:%M', menos:bool=True):
	naive_datetime = timezone.datetime.strptime(data, formato)
	aware_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())
	print('Aware: ', aware_datetime)
	# if menos:
	# 	aware_datetime = aware_datetime + timezone.timedelta(hours=3)
	# print('Aware: ', aware_datetime)
	return aware_datetime

@autenticado
def validaCadastrarReserva(request,funcionario:Funcionario=None):
	dataEntrada = request.POST['dataEntrada']
	hora = request.POST['hour']
	valor = request.POST['valor']
	cliente = Cliente.objects.get(id=request.POST['cliente'])
	quadra = Quadra.objects.get(id=request.POST['quadra'])
	horasReservada = request.POST['horasReservada']
	dt = datetime.strptime(dataEntrada + ' ' + hora, '%Y-%m-%d %H:%M')
	
	choque = verChoque(dt, quadra)
	# print(f'Choque: {choque}')

	if choque:
		# return redirect(f'/arena/verReservas/?status=1')
		statusCadastro = 1
		# redirect(f'/arena/home/?status = 0')
	
	else:
		# Ajustar a timezone do dt
		# print("Dt: ", dt)
		stringDt = dt.strftime('%Y-%m-%dT%H:%M')
		# print("StringDt: ", stringDt)
		# ajustadas = ajustarData(stringDt)
		# print("Ajustadas: ", ajustadas)

		novaReserva = Reserva(
			horaEntrada=stringDt, 
			horasReservada=horasReservada, 
			valor=float(valor), 
			cliente=cliente, 
			quadra=quadra
		)

		# print('Nova Reserva: ', novaReserva)
		novaReserva.save()
		# Verificar a hora diretamente no banco de dados
		reserva_salva = Reserva.objects.get(id=novaReserva.id)
		# print('reserva_salva:', reserva_salva)
		reserva_salva.horaEntrada -= timezone.timedelta(hours=3)
		# print('reserva_salva menos 3 hrs:', reserva_salva)
		reserva_salva.save()
		statusCadastro = 0

	return redirect(f'/arena/verReservas/?status={statusCadastro}')

def alugadas(data, quadra):
	reservas, algds = Reserva.objects.filter(horaEntrada__date=data, quadra=quadra), []
	print(f'\n\nReservas: {reservas} \n\n')
	for r in reservas:
		i, j = r.horaEntrada.hour, r.horasReservada
		while j > 0:
			algds.append(i) 
			i += 1
			j -= 1
		print(f'\n\nAlgds: {algds} \n\n')
	return algds

def verChoque(dt, quadra):
	# True: Chocou o horário.
	# False: O horário está livre.
	# return dt.hour in alugadas(dt.date(), quadra)
	alg = alugadas(dt.date(), quadra)
	print(alg)
	return dt.hour in alg


@autenticado
def reserva(request,id,funcionario:Funcionario=None):
	reserva = Reserva.objects.get(id=id)
	return render(request,'reserva.html', {'reserva': reserva})

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
		horasReservada = request.POST.get('horasReservada')
		horaSaida = request.POST.get('horaSaida')
		reserva.valor = valor
		reserva.quadra = Quadra.objects.get(id=tipo_quadra)
		reserva.horaEntrada = datetime.strptime(horaEntrada, '%Y-%m-%dT%H:%M')
		horasReservada = int(horasReservada)
		#reserva.horaSaida = datetime.strptime(horaSaida, '%Y-%m-%dT%H:%M')
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
		}
	)


@autenticado
def validaCadastrarPagamento(request, funcionario:Funcionario=None):
	forma = request.POST.get("forma")
	data = request.POST.get("data")
	reserva = request.POST.get("reserva")
	reservaBuscado = Reserva.objects.get(id=reserva)
	pagamento = Pagamento(forma=forma,data=data,reserva=reservaBuscado)
	pagamento.save()
	return redirect(f"/arena/home/?status=0")

@autenticado
def pagamento(request,id,funcionario:Funcionario=None):
	pagamento = Pagamento.objects.get(id=id)
	return render(request,'pagamento.html', {'pagamento': pagamento})

@autenticado
def excluirPagamento(request,id,funcionario:Funcionario=None):
	pagamento = Pagamento.objects.get(id=id)
	pagamento.delete()
	return redirect(f"/arena/verPagamento")


@autenticado
def editarPagamento(request, id, funcionario:Funcionario=None):
	pagamento = Pagamento.objects.get(id=id)
	reservas = Reserva.objects.all()
	return render(request, 'editarPagamento.html', {
		'pagamento': pagamento,
		'reservas': reservas,
		'funcionario': funcionario
	})

@autenticado
def validaEditarPagamento(request,id, funcionario:Funcionario=None):
	pagamento = Pagamento.objects.get(id=id)
	if request.method == 'POST':
		formaPag = request.POST.get('formaPag')
		valor = request.POST.get('valor')
		data = request.POST.get('data')
		reserva = request.POST.get('reserva')
		pagamento.forma= Pagamento.objects.get(id=formaPag)
		pagamento.valor = valor
		pagamento.data = datetime.strptime(data, '%Y-%m-%dT%H:%M')
		pagamento.save()
		return redirect('verPagamento')
	return render(request, 'editarPagamento.html', {
		'pagamento': pagamento,
		'funcionario': funcionario
	})