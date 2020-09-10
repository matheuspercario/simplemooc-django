from django.urls import path
# É preciso importar as 'views' desse próprio diretório (app)

from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('entrar/',
         auth_views.LoginView.as_view(template_name='accounts/login.html'),
         name="login"),
    path('sair/', auth_views.LogoutView.as_view(next_page='core:home'), name="logout"),
    path('cadastro/', views.register, name="register"),
    path('editar/', views.edit_account, name="edit_account"),
    path('alterar-senha/', views.change_password, name="change_password"),
    path('redefinir-senha/', views.password_reset, name="password_reset"),
    path('confirmar-redefinicao-senha/<slug:key>/',
         views.password_reset_confirm, name="password_reset_confirm"),
]
