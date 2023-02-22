from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .models import Account


def registration_view(request: HttpRequest) -> HttpResponse:
    form = RegistrationForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        new_user = Account.objects.create_user(username, email, password)
        new_user.save()

        messages.success(request, 'You have been registred.')
        return redirect('login')
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/registration.html', context)


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials.')
            

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout_view(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return redirect('/')
