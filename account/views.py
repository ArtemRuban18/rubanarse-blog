from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
from .forms import CustomPasswordResetForm

def register(request):
    """
    Views for user registration.

    If sigup_form is valid, create new user and redirect to login page.

    Context:
        - form: form for user registration
    
    Template:
        - register.html
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    context = {
        'form':form
    }
    return render(request, 'register.html', context)

def password_reset(request):
    """
    Views for password reset

    If password_reset is valid send email with link to reset password.

    Context:
        - password_reset_form: form for password reset
    Templates:
        - password_reset.html
    """
    if request.method == 'POST':
        password_reset_form = CustomPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            password_reset_form.save(request = request)
            return redirect('password_reset_done')
    else:
        password_reset_form = CustomPasswordResetForm()
    return render(request, 'password_reset.html', {'password_reset_form':password_reset_form})