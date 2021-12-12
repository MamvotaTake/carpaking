from django.shortcuts import render


def home(request):
    return render(request, 'account/login.html')
