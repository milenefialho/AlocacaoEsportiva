from django.urls import path
from . import views

urlpatterns = [
	path('login/', views.login, name = 'login'),
	path('cadastro/', views.cadastro, name = 'cadastro'),
	path('validaCadastro/', views.validaCadastro, name = 'validaCadastro'),
	path('validaLogin/', views.validaLogin, name = 'validaLogin'),
	path('home/', views.home, name = 'home'),
	path('sair/', views.sair, name = 'sair'),
	path('verEspaco/', views.verEspaco, name = 'verEspaco'),
	path('cadastrarEspaco/', views.cadastrarEspaco, name = 'cadastrarEspaco'),
	path('validaCadastrarEspaco/', views.validaCadastrarEspaco, name = 'validaCadastrarEspaco'),
	path('verCliente/', views.verCliente, name= 'verCliente'),
	path('cadastrarCliente/', views.cadastrarCliente, name = 'cadastrarCliente'),
	path('validaCadastrarCliente/', views.validaCadastrarCliente, name = 'validaCadastrarCliente'),
	path('verReservas/', views.verReservas, name = 'verReservas'),
	path('cadastrarReserva/', views.cadastrarReserva, name = 'cadastrarReserva'),
	path('validaCadastrarReserva/', views.validaCadastrarReserva, name = 'validaCadastrarReserva'),
	path('verPagamentos/', views.verPagamentos, name = 'verPagamentos'),
	path('cadastrarPagamento/', views.cadastrarPagamento, name = 'cadastrarPagamento'),
	path('validaCadastrarPagamento/', views.validaCadastrarPagamento, name = 'validaCadastrarPagamento'),
	path('excluirReserva/<int:id>', views.excluirReserva, name = 'excluirReserva'),
	path('reserva/<int:id>', views.reserva, name = 'reserva'),
	path('validaEditarReserva/<int:id>', views.validaEditarReserva, name = 'validaEditarReserva'),
	path('editarReserva/<int:id>', views.editarReserva, name = 'editarReserva'),
	path('excluirCliente/<int:id>', views.excluirCliente, name = 'excluirCliente'),
	path('cliente/<int:id>', views.cliente, name = 'cliente'),
	path('validaEditarCliente/<int:id>', views.validaEditarCliente, name = 'validaEditarCliente'),
	path('editarCliente/<int:id>', views.editarCliente, name = 'editarCliente'),
	path('excluirEspaco/<int:id>', views.excluirEspaco, name = 'excluirEspaco'),
	path('espaco/<int:id>', views.espaco, name = 'espaco'),
	path('validaEditarEspaco/<int:id>', views.validaEditarEspaco, name = 'validaEditarEspaco'),
	path('editarEspaco/<int:id>', views.editarEspaco, name = 'editarEspaco')

]


