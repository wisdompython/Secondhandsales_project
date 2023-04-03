from django.shortcuts import render, redirect
from .forms import CustomLoginForm, Register, SetPasswordForm
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    form = Register()
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            form.save()
            return redirect('product-list')
            
        else:
            print(form.errors)

    return render(request, 'registration/signup.html',{'form':form})

