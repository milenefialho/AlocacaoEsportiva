from django.db import models
from datetime import datetime


class Arena(models.Model):
	nome = models.CharField(max_length = 100)
	cnpj = models.CharField(max_length = 20)

	def __str__(self):
		return f"{self.nome} - {self.cnpj}"

class Endereco(models.Model):
	estado = models.CharField(max_length = 50)
	cidade = models.CharField(max_length = 50)
	bairro = models.CharField(max_length = 50)
	rua = models.CharField(max_length = 100)
	numero = models.CharField(max_length = 10,blank=True,default="S/N")
	complemento = models.CharField(max_length = 100,blank=True,default="")

	def __str__(self):
		return self.estado


class Funcionario(models.Model):
	admin = models.BooleanField(default = False)
	arena = models.ForeignKey(Arena, on_delete=models.CASCADE)
	senha = models.CharField(max_length = 50, default = "")
	nome = models.CharField(max_length = 50, default = "")
	telefone = models.CharField(max_length = 20, default = "")
	cpf = models.CharField(max_length = 20, default = "")
	email = models.CharField(max_length = 50, default = "")
	endereco = models.IntegerField(default = -1)

	def __str__(self):
		return self.nome

class Cliente(models.Model):
	nome = models.CharField(max_length = 50, default = "")
	telefone = models.CharField(max_length = 20, default = "")
	cpf = models.CharField(max_length = 20, default = "")
	email = models.CharField(max_length = 50, default = "")
	endereco = models.IntegerField(default = -1)

	def __str__(self):
		return self.nome



class Quadra(models.Model):
	tipo = models.CharField(max_length = 20)
	preco = models.FloatField(default=0.0) # preco por hr da quadra
	reservado = models.BooleanField(default=False)
	

	def __str__(self):
		return f"{self.tipo} - {self.preco}"

class Reserva(models.Model):
	horaEntrada = models.DateTimeField(default=datetime.now, blank=True)
	horaSaida = models.DateTimeField(default=datetime.now, blank=True)
	valor = models.FloatField(default=0.0)
	cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
	quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE, default = None)
	status =models.BooleanField(default=False)

	def __str__(self):
		return f"{self.cliente} - {self.horaEntrada} - {self.valor}"

class Pagamento(models.Model):
	forma = models.CharField(max_length = 20)
	valor = models.FloatField(default=0.0) # valor pago pelo cliente
	data = models.DateTimeField(default=datetime.now, blank=True)
	reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE,related_name='pagamento')


	def __str__(self):
		return f"{self.forma} - {self.valor}"
