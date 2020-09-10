from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from core.utils import generate_hash_key
from core.mail import send_mail_template
from . models import PasswordReset

User = get_user_model()

# Estou dizendo que 'RegisterForm' HERDA 'UserCreationForm'


class RegisterForm(forms.ModelForm):
    # Novos atributos
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmação de senha', widget=forms.PasswordInput
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas não são idênticas')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email']


class EditAccountForm(forms.ModelForm):

    class Meta:
        model = User
        # fields = ['username', 'email', 'first_name', 'last_name']
        fields = ['username', 'email', 'name']


class PasswordResetForm(forms.Form):
    # Validar se o email informado esta cadastrado
    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            return email
        raise forms.ValidationError(
            'Não existe usuário com este E-mail cadastrado')

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(user=user, key=key)
        reset.save()
        template_name = 'accounts/password_reset_email.html'
        subject = '[REDEFINIR SENHA] - Simple Mooc'
        context = {
            'reset': reset
        }
        send_mail_template(subject, template_name, context, [user.email])
