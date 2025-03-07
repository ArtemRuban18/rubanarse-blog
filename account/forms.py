from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings


class RegisterForm(UserCreationForm):
    """
    Form for user`s registration

    Fields:
        - username: CharField
        - email: EmailField
        - password1: CharField
        - password2: CharField
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username':'Ім\'я Прізвище',
            'email':'Email',
            'password1':'Введіть пароль',
            'password2':'Повторіть пароль'
        }

        help_texts = {
            'username':None,
            'email':None,
            'password1':None,
            'password2':None,
        }

        def check_password(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')

            if password1 != password2 and password1 and password2:
                return forms.ValidationError('Паролі не збігаються!')
            
class CustomPasswordResetForm(PasswordResetForm):
    """
    Form for password reset

    Fields:
        - email: EmailField
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={"autocomplete": "email"})
    
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        context['domain'] = settings.DEFAULT_DOMAIN
        context['protocol'] = settings.DEFAULT_PROTOCOL
        super().send_mail(subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name)
