from core.mail import send_mail_template
from django.conf import settings
from django.db import models
from django.urls import reverse
from _datetime import date, datetime

# Create your models here.


class CourseQuerySet(models.QuerySet):
    def search(self, query):
        return self.filter(
            models.Q(name__icontains=query) | models.Q(description__icontains=query)
        )


class Course(models.Model):

    name = models.CharField("Nome", max_length=100)
    slug = models.SlugField("Atalho")
    description = models.TextField("Descrição Simples", blank=True)
    about = models.TextField("Sobre o curso", blank=True)
    start_date = models.DateField("Data de início", null=True, blank=True)
    image = models.ImageField(
        upload_to="courses/images", verbose_name="Imagem", null=True, blank=True
    )
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    # necessario para criar meu próprio manager com 'search'
    objects = CourseQuerySet.as_manager()

    # método que auxilia a ida para página de detalhe
    def get_absolute_url(self):
        return reverse("courses:details", args=(self.slug,))

    def release_lessons(self):
        today = date.today()
        # lte - menor ou igual a hoje
        # gte - maior ou igual a hoje
        return self.lessons.filter(release_date__lte=today)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["name"]


class Lesson(models.Model):

    course = models.ForeignKey(
        Course, verbose_name="Curso", related_name="lessons", on_delete=models.CASCADE
    )

    name = models.CharField(("Nome"), max_length=100)
    description = models.TextField(("Descrição"), blank=True)
    number = models.IntegerField(("Número (ordem)"), blank=True, default=0)
    release_date = models.DateField(("Data de Liberação"), blank=True, null=True)

    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def is_avaliable(self):
        if self.release_date:
            today = date.today()
            return self.release_date <= today
        return False

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"
        ordering = ["number"]


class Material(models.Model):

    lesson = models.ForeignKey(
        Lesson,
        verbose_name="Material",
        related_name="materials",
        on_delete=models.CASCADE,
    )

    name = models.CharField(("Nome"), max_length=100)
    embedded = models.TextField(("Vídeo embedded"), blank=True)
    file = models.FileField(
        (""), upload_to="lessons/materials", blank=True, null=True, max_length=100
    )

    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiais"


class Enrollment(models.Model):
    # Modelagem da inscrição do aluno em um curso
    STATUS_CHOICE = (
        (0, "Pendente"),
        (1, "Aprovado"),
        (2, "Cancelado"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course,
        verbose_name="Curso",
        related_name="enrollments",
        on_delete=models.CASCADE,
    )
    status = models.IntegerField(
        "Situação", choices=STATUS_CHOICE, default=0, blank=True
    )
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def active(self):
        # Ativar a inscrição do aluno no curso
        self.status = 1
        self.save()

    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name = "Inscrição"
        verbose_name_plural = "Inscrições"
        unique_together = (("user", "course"),)


class Announcement(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="announcements",
        verbose_name="Curso",
        on_delete=models.CASCADE,
    )
    title = models.CharField("Título", max_length=100)
    content = models.TextField("Conteúdo")

    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Anúncio"
        verbose_name_plural = "Anúncios"
        ordering = ["-created_at"]


class Comment(models.Model):
    announcement = models.ForeignKey(
        Announcement,
        related_name="comments",
        verbose_name="Anúncio",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="usuário", on_delete=models.CASCADE
    )
    comment = models.TextField("Comentário")

    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ["created_at"]


def post_save_announcement(instance, created, **kwargs):
    template_name = "courses/announcement_mail.html"
    subject = instance.title
    context = {"announcement": instance}
    enrollments = Enrollment.objects.filter(course=instance.course, status=1)
    for enrollment in enrollments:
        recipient_list = [enrollment.user.email]
        send_mail_template(subject, template_name, context, recipient_list)


models.signals.post_save.connect(
    post_save_announcement, sender=Announcement, dispatch_uid="post_save_announcement"
)
