from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from .models import Funcionario,Endereco,Arena,Quadra
from django.contrib import messages
from django.shortcuts import redirect 
from hashlib import sha256
from django.contrib.auth import authenticate, login


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

    email = request.POST.get('email')
    senha = request.POST.get('senha')
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
			retorno = funcao(request, funcionario, *args, **kwargs)
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
	quadras = list(Quadra.objects.filter())
	return render(request,'verEspaco.html', {
		'nome': funcionario.nome,
		'qnt': len(quadras)
		}
	)

@autenticado
def cadastrarEspaco(request, funcionario:Funcionario=None):
	return render(request,'cadastrarEspaco.html', {'nome': funcionario.nome})

@autenticado
def validaCadastrarEspaco(request, funcionario:Funcionario=None):
	tipo = request.POST.get('tipo')
	valor = request.POST.get('valor')

	if tipo == " ": 
		return redirect(f'/arena/cadastrarEspaco/?status = 1')
	else:
		quadra = Quadra(tipo=tipo,preco=float(valor),reservado = False)
		quadra.save()
	return redirect(f'/arena/verEspaco/?status = 0')






	
