from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.core import validators
from django.conf import settings


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Usuários precisam cadastrar um 'E-mail'")
        if not username:
            raise ValueError(
                "Usuários precisam cadastrar um 'Nome de usuário'.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    # Campos personalizaveis
    username = models.CharField(
        verbose_name='Nome de usuário',
        max_length=30,
        unique=True,
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                'Usuário inválido',
                'invalid'
            )
        ]
    )
    email = models.EmailField(verbose_name='E-mail', unique=True)
    name = models.CharField('Nome completo', max_length=100, blank=True)

    # Campos necessarios
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(
        verbose_name='Último login', auto_now=True)
    date_joined = models.DateTimeField(
        verbose_name='Data cadastro', auto_now_add=True)

    USERNAME_FIELD = 'username'  # Referencia para login do Django
    REQUIRED_FIELDS = ['email', ]  # Dizer que o email é sempre necessario

    # Necessario para algumas coisas do Django
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    # def get_short_name(self):
    #     return self.username

    # def get_full_name(self):
    #     return self(str)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class PasswordReset(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='resets',
    )
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    confirmed = models.BooleanField('Status', default=False, blank=True)

    def __str__(self):
        return f'{self.user} - {self.created_at}'

    class Meta:
        verbose_name = 'Nova senha'
        verbose_name_plural = 'Novas senhas'
        ordering = ['-created_at']
