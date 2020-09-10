from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings
from django.urls import reverse

# Create your models here.


class Topic(models.Model):
    title = models.CharField(('Título'), max_length=100)
    slug = models.SlugField(('Identificador'), max_length=100, unique=True)
    body = models.TextField(('Mensagem'))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=('Autor'),
        on_delete=models.CASCADE,
    )
    views = models.IntegerField(('Visualizações'), blank=True, default=0)
    answers = models.IntegerField(('Respostas'), blank=True, default=0)

    tags = TaggableManager()

    created = models.DateTimeField(('Criado em'), auto_now_add=True)
    modified = models.DateTimeField(('Modificado em'), auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("forum:topic", args=(self.slug,))

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-modified']


class Reply(models.Model):
    reply = models.TextField(('Resposta'))
    topic = models.ForeignKey(
        Topic,
        verbose_name=('Tópico'),
        related_name='replies',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=('Autor'),
        on_delete=models.CASCADE,
    )

    correct = models.BooleanField(
        ('Melhor resposta'), blank=True, default=False
    )

    created = models.DateTimeField(('Criado em'), auto_now_add=True)
    modified = models.DateTimeField(('Modificado em'), auto_now=True)

    def __str__(self):
        return self.reply[:100]

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-correct', 'created']

# ------------------------------------------------------
# SIGNALS
# ------------------------------------------------------


def post_save_reply(instance, **kwargs):
    instance.topic.answers = instance.topic.replies.count()
    instance.topic.save()
    if instance.correct:
        instance.topic.replies.exclude(pk=instance.pk).update(correct=False)


def post_delete_reply(instance, **kwargs):
    instance.topic.answers = instance.topic.replies.count()
    instance.topic.save()


models.signals.post_save.connect(
    post_save_reply, sender=Reply, dispatch_uid='post_save_reply'
)
models.signals.post_delete.connect(
    post_delete_reply, sender=Reply, dispatch_uid='post_delete_reply'
)
