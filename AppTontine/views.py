from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')


def Cotiser(request):
    return render(request, 'Cotiser.html')