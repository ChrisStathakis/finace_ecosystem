from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib import messages

from .forms import LoginForm

# Create your views here.


def login_view(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponseRedirect('/')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            messages.warning(request,  'Ο κωδικός ή το email είναι λάθος.')
    return render(request, 'login.html', context={'form': form})
