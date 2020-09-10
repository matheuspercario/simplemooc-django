from django.urls import path

# É preciso importar as 'views' desse próprio diretório (app)
from . import views

app_name = "forum"

urlpatterns = [
    path("", views.ForumView.as_view(), name="forum_index"),
    path("tag=<slug:tag>", views.ForumView.as_view(), name="index_taggit"),
    path("topico/<slug:slug>", views.TopicView.as_view(), name="topic"),
]
