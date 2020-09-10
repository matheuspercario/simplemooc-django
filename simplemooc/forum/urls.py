from django.urls import path

# É preciso importar as 'views' desse próprio diretório (app)
from . import views

app_name = "forum"

urlpatterns = [
    path("", views.ForumView.as_view(), name="forum_index"),
    path("tag=<slug:tag>", views.ForumView.as_view(), name="index_taggit"),
    path("respostas/<int:pk>/correta/",
         views.ReplyChooseView.as_view(), name="reply_correct"),
    path("respostas/<int:pk>/incorreta/",
         views.ReplyChooseView.as_view(correct=False), name="reply_incorrect"),
    path("topico/<slug:slug>", views.TopicView.as_view(), name="topic"),

]
