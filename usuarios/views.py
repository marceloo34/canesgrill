from django.shortcuts import render

# Create your views here.
'''
urlpatterns = [
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
]

'''

def cadastro(request):
    return render(request, 'cadastro.html')


def login(request):
    return render(request, 'login.html')


def dashboard(request):
    ...


def logout(request):
    ...
