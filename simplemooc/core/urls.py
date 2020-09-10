from django.urls import path

# É preciso importar as 'views' desse próprio diretório (app)
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("contato/", views.contact, name="contact"),
]
