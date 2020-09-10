from django import forms
from django.core.mail import send_mail
from django.conf import settings

from core.mail import send_mail_template

from . models import Comment

# Create your forms here


class ContactForm(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail')
    message = forms.CharField(label='Mensagem / Dúvida', widget=forms.Textarea)

    def send_mail(self, course):
        subject = f'[{course}] Contato'
        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'],
        }
        template_name = 'courses/contact_email.html'
        send_mail_template(subject, template_name, context,
                           [settings.CONTACT_EMAIL])


class CommentForm(forms.ModelForm):

    def form_save(self, user, announcement):
        comment = self.save(commit=False)
        # Preciso inserir antes de salvar, caso contrário não há usuário
        # e nem inscricao para salvar
        comment.user = user
        comment.announcement = announcement
        comment.save()

    class Meta():
        model = Comment
        fields = ['comment', ]
