from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from random import randint
from churras.models import Prato

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
    if request.method == 'POST':
        
        nome = request.POST['nome_completo'].title()
        email = request.POST['email']
        senha = request.POST['senha']
        senha2 = request.POST['senha2']
        nome_completo = nome.split()
        user_name = nome.replace(' ', '')
        user_name = user_name.lower()
        
        if not nome.strip():
            print('O campo Nome Completo não pode ficar em branco.')
            nome = nome.strip()
            return redirect('cadastro')
        
        if not email.strip():
            print('O campo Email não pode ficar em branco.')
            email = email.strip()
            return redirect('cadastro')
        
        if senha != senha2 or not senha.strip() or not senha2.strip():
            print('As senha não são iguais ou uma delas está em branco.')
            return redirect('cadastro')
        
        if User.objects.filter(email=email).exists():
            print('Email já cadastrado.')
            return redirect('cadastro')
        
        if User.objects.filter(username=user_name).exists():
            print(f'Username {user_name} já cadastrado.')
            user_name = f'{user_name}{randint(1000, 9999)}'
            pass


        if len(nome_completo) > 1:
            primeiro_nome = nome_completo[0]
            segundo_nome = nome_completo[-1]
        else:
            primeiro_nome = nome_completo[0]
            segundo_nome = ''
        
        user = User.objects.create_user(username=user_name, email=email, password=senha, first_name=primeiro_nome, last_name=segundo_nome)
        user.save()
        print('Usuário cadastrado com sucesso.')
        return redirect('login')
    
    return render(request, 'cadastro.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        # print(f'POST: {request.POST}')
        
        email = request.POST['email']
        senha = request.POST['senha']
        
        if email == '' or senha == '':
            print('Os campos de email e senha não podem ficar em branco.')
            return redirect('login')
        
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            
            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso.')
                return render(request, 'dashboard.html')

        print('Usuário e/ou Senha inválidos.')
        return redirect('login')
        
    return render(request, 'login.html')


def dashboard(request):
    if request.user.is_authenticated:
        pratos = Prato.objects.filter(publicado=True).order_by('-date_prato')
    
        contexto = {
        'lista_pratos': pratos,
    }
        
        return render(request, 'dashboard.html', contexto)
    
    return redirect('index')


def logout(request):
    auth.logout(request)
    print('Você realizou o logout')
    return redirect('index')


def cria_prato(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            nome_prato = request.POST['nome_prato'].strip().title()
            ingredientes = request.POST['ingredientes']
            modo_preparo = request.POST['modo_preparo']
            tempo_preparo = request.POST['tempo_preparo']
            rendimento = request.POST['rendimento']
            categoria = request.POST['categoria']
            foto_prato = request.FILES['foto_prato']
            
            
        
        
        
        
        return render(request, 'cria_prato.html')
    return redirect('index')
