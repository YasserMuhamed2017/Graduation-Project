from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'hotel/index.html')

def login_view(request):
    return render(request, 'hotel/login.html')

def register_view(request):
    return render(request, 'hotel/register.html')