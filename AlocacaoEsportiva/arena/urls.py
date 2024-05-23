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
	path('validaCadastrarEspaco/', views.validaCadastrarEspaco, name = 'validaCadastrarEspaco')


]


