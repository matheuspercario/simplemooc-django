from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import enrollment_required
from .forms import CommentForm, ContactForm
from .models import Announcement, Course, Enrollment, Lesson, Material

# Create your views here.


def main_courses(request):
    template_name = "courses/main_courses.html"
    courses = Course.objects.all()
    context = {"courses": courses}
    return render(request, template_name, context)


def details(request, slug):
    template_name = "courses/details.html"
    course = get_object_or_404(Course, slug=slug)
    context = {}  # Criar dicionário do contexto
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            context["is_valid"] = True  # Contexto passou pela validação
            # Chamando funcao que envia email da classe 'ContactForm'
            form.send_mail(course)
            # print(form.cleaned_data['name'])  # Printar no console as informações do POST já validadas
            # print(form.cleaned_data['email'])
            # print(form.cleaned_data['message'])
            form = ContactForm()  # Limpar o formulário após validacao
    else:
        form = ContactForm()
    context["form"] = form  # Adicionar o formulario ao contexto
    context["course"] = course  # Adicionar o curso ao contexto
    return render(request, template_name, context)


@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,  # Usuário atual
        course=course,  # Curso em questão
    )
    if created:
        enrollment.active()
        messages.success(request, "Inscrição realizada com sucesso!")
    else:
        messages.info(request, "Já está inscrito neste curso.")
    return redirect("accounts:dashboard")


@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=course,
    )
    if request.method == "POST":
        enrollment.delete()
        messages.success(request, "Sua inscrição foi cancelada com sucesso!")
        return redirect("accounts:dashboard")
    template_name = "courses/undo_enrollment.html"
    context = {"enrollment": enrollment, "course": course}
    return render(request, template_name, context)


@login_required
@enrollment_required
def announcements(request, slug):
    course = request.course
    # course = get_object_or_404(Course, slug=slug)
    # if not request.user.is_staff:
    #     enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    #     if not enrollment.is_approved():
    #         messages.error(request, "Inscrição cancelada ou pendente.")
    #         return redirect("accounts:dashboard")
    template_name = "courses/announcements.html"
    context = {
        "course": course,
        "announcements": course.announcements.all(),
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    course = request.course
    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        form.form_save(request.user, announcement)
        messages.success(request, "Comentário enviado com sucesso!")
        form = CommentForm()
    template_name = "courses/show_announcement.html"
    context = {
        "course": course,
        "announcement": announcement,
        "form": form,
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    lessons = course.release_lessons()
    if request.user.is_staff:
        lessons = course.lessons.all()
    template_name = "courses/lessons.html"
    context = {
        "course": course,
        "lessons": lessons,
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def show_lesson(request, slug, pk):
    course = request.course
    lesson = get_object_or_404(Lesson, pk=pk, course=course)
    if not request.user.is_staff and not lesson.is_avaliable():
        messages.error(request, "Está aula não está disponível")
        return redirect("courses:lessons", slug=course.slug)
    template_name = "courses/show_lesson.html"
    context = {
        "course": course,
        "lesson": lesson,
    }
    return render(request, template_name, context)


@login_required
@enrollment_required
def material(request, slug, pk):
    course = request.course
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson
    if not request.user.is_staff and not lesson.is_avaliable():
        messages.error(request, "Este material não está disponível")
        return redirect("courses:lessons", slug=course.slug, pk=lesson.pk)
    if not material.is_embedded():
        # Se nao houver nada imbutido e mesmo asim o usuário tentar acessar via URl, redirecione ao embutido
        return redirect(material.file.url)
    template_name = "courses/material.html"
    context = {
        "course": course,
        "lesson": lesson,
        "material": material,
    }
    return render(request, template_name, context)