from django.urls import path

# É preciso importar as 'views' desse próprio diretório (app)
from . import views

app_name = "courses"

urlpatterns = [
    path("", views.main_courses, name="main_courses"),
    path("<slug:slug>/", views.details, name="details"),
    path("<slug:slug>/inscricao/", views.enrollment, name="enrollment"),
    path(
        "<slug:slug>/cancelar-inscricao/", views.undo_enrollment, name="undo_enrollment"
    ),
    path("<slug:slug>/anuncios/", views.announcements, name="announcements"),
    path(
        "<slug:slug>/anuncios/<int:pk>/",
        views.show_announcement,
        name="show_announcement",
    ),
    path("<slug:slug>/aulas/", views.lessons, name="lessons"),
    path("<slug:slug>/aulas/<int:pk>/", views.show_lesson, name="show_lesson"),
    path("<slug:slug>/material/<int:pk>/", views.material, name="material"),
]
