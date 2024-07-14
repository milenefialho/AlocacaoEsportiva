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

#Segunda versao ----------------------------------------------

def reservasSobrepostas(horaEntrada: datetime,horaSaida: datetime,quadraId: int) -> bool:

	reservasExistentes = Reserva.objects.filter(quadra_id=quadraId)
    
	for reservaExistente in reservasExistentes:
		horaEntradaExi = reservaExistente.horaEntrada.replace(tzinfo=None)
		horaSaidaExi = reservaExistente.horaSaida.replace(tzinfo=None)

		if (
			horaEntrada < horaSaidaExi
			and horaSaida < horaEntradaExi
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
	clienteId = request.POST.get("cliente")
	quadraId = request.POST.get("quadra")
	status = request.POST.get("status")

	# Adicionando prints para depuração
	print(f"horaEntrada: {horaEntrada}, horaSaida: {horaSaida}, valor: {valor}, cliente: {cliente}, quadraId: {quadraId}")


	# Verifica se todos os campos obrigatórios foram preenchidos
	if not all([horaEntrada, horaSaida, valor, cliente, quadraId]):
		return render(request, 'cadastrarReserva.html', {
			'error': 'Por favor, preencha todos os campos obrigatórios.',
			'clientes': Cliente.objects.all(),
			'quadras': Quadra.objects.all()
		})


	horaEntradaObj = converteHorarios(horaEntrada).replace(tzinfo=None)
	horaSaidaObj = converteHorarios(horaSaida).replace(tzinfo=None)

	if reservasSobrepostas(horaEntrada=horaEntradaObj, horaSaida=horaSaidaObj, quadraId=int(quadraId)):
		return render(request, 'cadastrarReserva.html', {
			'error': 'Já existe uma reserva para este horário e quadra.',
			'clientes': Cliente.objects.all(),
			'quadras': Quadra.objects.all()
		})
     
	clienteBuscado = Cliente.objects.get(id=int(clienteId))
	quadraBuscada = Quadra.objects.get(id=int(quadraId))

	reserva = Reserva(horaEntrada=horaEntradaObj,
		horaSaida=horaSaidaObj,
		valor=float(valor),
		cliente= clienteBuscado,
		quadra= quadraBuscada)
	reserva.save()
	return redirect(f"/arena/home/?status=0")