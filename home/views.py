from django.shortcuts import render, redirect


def home(request):
    return redirect('register')


def register(request):
    return render(request, "home/register.html")
