from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from random import randint
from churras.models import Prato


def campo_vazio(campo):
    return not campo.strip()


def senhas_diferentes(senha, senha2):
    return senha != senha2

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
        if len(nome_completo) > 1:
                primeiro_nome = nome_completo[0]
                segundo_nome = nome_completo[-1]
        else:
                primeiro_nome = nome_completo[0]
                segundo_nome = ''
        nome_user = primeiro_nome + segundo_nome
        # user_name = nome.replace(' ', '')
        user_name = nome_user.lower()
        
        if campo_vazio(nome):
            messages.error(request, 'O campo Nome Completo não pode ficar em branco.')
            nome = nome.strip()
            return redirect('cadastro')
        
        if campo_vazio(email):
            messages.error(request, 'O campo Email não pode ficar em branco.')
            email = email.strip()
            return redirect('cadastro')
        
        
        
        if senhas_diferentes(senha, senha2) or campo_vazio(senha) or campo_vazio(senha2):
            messages.error(request, 'As senha não são iguais ou uma delas está em branco.')
            return redirect('cadastro')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado.')
            return redirect('cadastro')
        
        if User.objects.filter(username=user_name).exists():
            user_name2 = f'{user_name}{randint(1000, 9999)}'
            user = User.objects.create_user(username=user_name2, email=email, password=senha, first_name=primeiro_nome, last_name=segundo_nome)
            user.save()
            messages.info(request, f'Usuário {user_name} já cadastrado. Foi gerado o Usuário {user_name2} automaticamente.')
            return redirect('login')
        
        user = User.objects.create_user(username=user_name, email=email, password=senha, first_name=primeiro_nome, last_name=segundo_nome)
        user.save()
        messages.success(request, f'Usuário {user_name} cadastrado com sucesso.')
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
            messages.error(request, 'Os campos de email e senha não podem ficar em branco.')
            return redirect('login')
        
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso.')
                return redirect('dashboard')

        messages.error(request, 'Usuário e/ou Senha inválidos.')
        return redirect('login')
        
    return render(request, 'login.html')


def dashboard(request):
    if request.user.is_authenticated:
        pratos = Prato.objects.filter(pessoa=request.user.id).order_by('-date_prato')
    
        contexto = {
        'lista_pratos': pratos,
    }
        
        return render(request, 'dashboard.html', contexto)
    
    messages.error(request, 'Você não tem permissão para acessar o Dashboard.')
    return redirect('index')


def logout(request):
    auth.logout(request)
    messages.success(request, 'Você realizou o logout')
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
            user = get_object_or_404(User, pk=request.user.id)
            
            
            prato = Prato.objects.create(
                nome_prato=nome_prato,
                ingredientes=ingredientes,
                modo_preparo=modo_preparo,
                tempo_preparo=tempo_preparo,
                rendimento=rendimento,
                categoria=categoria,
                foto_prato=foto_prato,
                pessoa=user
            )
            prato.save()
            messages.success(request, 'Prato criado com sucesso.')
            return redirect('dashboard')
                    
        return render(request, 'cria_prato.html')
    
    messages.error(request, 'Você não tem permissão para criar pratos.')
    return redirect('index')


def deleta_prato(request, prato_id):
    if request.user.is_authenticated:
        try:
            prato = get_object_or_404(Prato, pk=prato_id)
            nome_prato = prato.nome_prato
            prato.delete()        
            messages.success(request, f'Prato "{nome_prato}" excluído com sucesso.')
            return redirect('dashboard')
        except:
            messages.error(request, 'Prato não encontrado.')
            return redirect('dashboard')
    
    
    messages.error(request, 'Você não tem permissão para apagar pratos.')
    return redirect('index')


def edita_prato(request, prato_id):
    if request.user.is_authenticated:
        try:
            prato = get_object_or_404(Prato, pk=prato_id)
        except:
            messages.error(request, 'Prato não encontrado.')
            return redirect('dashboard')
    
        contexto = {
            'prato': prato,
        }
        
        return render(request, 'edita_prato.html', contexto)
    
    messages.error(request, 'Você não ter permissão para editar pratos.')
    return redirect('index')


def atualiza_prato(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            prato_id = request.POST['prato_id']
            nome_prato = request.POST['nome_prato'].strip().title()
            ingredientes = request.POST['ingredientes']
            modo_preparo = request.POST['modo_preparo']
            tempo_preparo = request.POST['tempo_preparo']
            rendimento = request.POST['rendimento']
            categoria = request.POST['categoria']
            
            prato = Prato.objects.get(pk=prato_id)
            prato.nome_prato = nome_prato
            prato.ingredientes = ingredientes
            prato.modo_preparo = modo_preparo
            prato.tempo_preparo = tempo_preparo
            prato.rendimento = rendimento
            prato.categoria = categoria
            if 'foto_prato' in request.FILES:
                prato.foto_prato = request.FILES['foto_prato']
                
            prato.save()
            messages.success(request, f'Prato "{nome_prato}" modificado com sucesso.')
            return redirect('dashboard')
                    
        return redirect('dashboard')
    
    messages.error(request, 'Você não tem permissão para alterar pratos.')
    return redirect('index')