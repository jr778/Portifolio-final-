#!/usr/bin/env python3
"""
App de Segurança da Informação - Django + Cryptography
Aplicativo funcional para armazenamento seguro de dados sensíveis
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import base64

# Configuração do Django
if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'seguranca.db',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'seguranca',
        ],
        SECRET_KEY='django-insecure-seguranca-app-key-2024',
        ROOT_URLCONF='app_seguranca',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(os.path.dirname(__file__), 'templates')],
            },
        ],
        STATIC_URL='/static/',
        DEBUG=True,
    )

# Modelo para dados sensíveis
class DadosSensiveis(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    dados_criptografados = models.BinaryField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def set_dados(self, dados):
        """Criptografa e armazena dados"""
        key = Fernet.generate_key()
        cipher = Fernet(key)
        self.dados_criptografados = cipher.encrypt(dados.encode())
    
    def get_dados(self, key):
        """Descriptografa dados usando a chave"""
        cipher = Fernet(key)
        return cipher.decrypt(self.dados_criptografados).decode()

# Views do aplicativo
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse

@login_required
def dashboard(request):
    """Dashboard principal do aplicativo"""
    dados = DadosSensiveis.objects.filter(usuario=request.user)
    return render(request, 'dashboard.html', {
        'dados': dados,
        'usuario': request.user
    })

@login_required
def adicionar_dado(request):
    """Adiciona novo dado sensível"""
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        dados = request.POST.get('dados')
        
        if titulo and dados:
            dado = DadosSensiveis(usuario=request.user, titulo=titulo)
            dado.set_dados(dados)
            dado.save()
            return redirect('dashboard')
    
    return render(request, 'adicionar.html')

def registrar(request):
    """Registro de usuário"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'registrar.html', {'form': form})

# URLs do aplicativo
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('adicionar/', adicionar_dado, name='adicionar_dado'),
    path('registrar/', registrar, name='registrar'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Templates HTML
def criar_templates():
    """Cria os templates HTML necessários"""
    templates_dir = 'templates'
    os.makedirs(templates_dir, exist_ok=True)
    
    # Template base
    base_html = '''<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}App Segurança{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .header { background: #2c3e50; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .btn { padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; }
        .btn-danger { background: #e74c3c; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; }
        .form-group input, .form-group textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        .dado-item { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 App de Segurança da Informação</h1>
            <p>Bem-vindo, {{ usuario.username }} | <a href="{% url 'logout' %}" style="color: white;">Logout</a></p>
        </div>
        {% block content %}{% endblock %}
    </div>
</body>
</html>'''
    
    # Dashboard template
    dashboard_html = '''{% extends "base.html" %}
{% block content %}
<h2>📊 Dashboard - Seus Dados Seguros</h2>
<a href="{% url 'adicionar_dado' %}" class="btn">➕ Adicionar Novo Dado</a>

{% if dados %}
    <h3>Dados Armazenados:</h3>
    {% for dado in dados %}
    <div class="dado-item">
        <h4>{{ dado.titulo }}</h4>
        <p><strong>Data:</strong> {{ dado.data_criacao|date:"d/m/Y H:i" }}</p>
        <p><strong>Status:</strong> ✅ Criptografado e Seguro</p>
    </div>
    {% endfor %}
{% else %}
    <p>Nenhum dado sensível armazenado ainda.</p>
{% endif %}
{% endblock %}'''
    
    # Adicionar template
    adicionar_html = '''{% extends "base.html" %}
{% block content %}
<h2>➕ Adicionar Dado Sensível</h2>
<form method="post">
    {% csrf_token %}
    <div class="form-group">
        <label>Título:</label>
        <input type="text" name="titulo" required>
    </div>
    <div class="form-group">
        <label>Dados Sensíveis:</label>
        <textarea name="dados" rows="5" required placeholder="Digite os dados sensíveis aqui..."></textarea>
    </div>
    <button type="submit" class="btn">🔐 Salvar Criptografado</button>
    <a href="{% url 'dashboard' %}" class="btn btn-danger">Cancelar</a>
</form>
{% endblock %}'''
    
    # Login template
    login_html = '''{% extends "base.html" %}
{% block content %}
<h2>🔑 Login</h2>
<form method="post">
    {% csrf_token %}
    <div class="form-group">
        <label>Usuário:</label>
        <input type="text" name="username" required>
    </div>
    <div class="form-group">
        <label>Senha:</label>
        <input type="password" name="password" required>
    </div>
    <button type="submit" class="btn">Entrar</button>
</form>
<p>Não tem conta? <a href="{% url 'registrar' %}">Registrar</a></p>
{% endblock %}'''
    
    # Registrar template
    registrar_html = '''{% extends "base.html" %}
{% block content %}
<h2>📝 Registrar Nova Conta</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn">Registrar</button>
</form>
<p>Já tem conta? <a href="{% url 'login' %}">Login</a></p>
{% endblock %}'''
    
    # Salvar templates
    with open(f'{templates_dir}/base.html', 'w', encoding='utf-8') as f:
        f.write(base_html)
    
    with open(f'{templates_dir}/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    with open(f'{templates_dir}/adicionar.html', 'w', encoding='utf-8') as f:
        f.write(adicionar_html)
    
    with open(f'{templates_dir}/login.html', 'w', encoding='utf-8') as f:
        f.write(login_html)
    
    with open(f'{templates_dir}/registrar.html', 'w', encoding='utf-8') as f:
        f.write(registrar_html)

# Arquivo de configuração do Django
def criar_settings():
    """Cria o arquivo settings.py"""
    settings_content = '''import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-seguranca-app-key-2024'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'seguranca',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app_seguranca.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app_seguranca.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'seguranca.db',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
'''
    
    with open('settings.py', 'w', encoding='utf-8') as f:
        f.write(settings_content)

# Arquivo de URLs principal
def criar_urls_principal():
    """Cria o arquivo urls.py principal"""
    urls_content = '''from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('seguranca.urls')),
]
'''
    
    with open('urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_content)

# Arquivo manage.py
def criar_manage():
    """Cria o arquivo manage.py"""
    manage_content = '''#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
'''
    
    with open('manage.py', 'w', encoding='utf-8') as f:
        f.write(manage_content)

# Requirements.txt
def criar_requirements():
    """Cria o arquivo requirements.txt"""
    requirements = '''Django==4.2.7
cryptography==41.0.7
'''
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)

# README.md
def criar_readme():
    """Cria o arquivo README.md"""
    readme = '''# 🔐 App de Segurança da Informação

Aplicativo Django funcional para armazenamento seguro de dados sensíveis usando criptografia Fernet.

## 🚀 Instalação

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

2. **Executar migrações:**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Criar superusuário (opcional):**
```bash
python manage.py createsuperuser
```

4. **Executar servidor:**
```bash
python manage.py runserver
```

5. **Acessar aplicativo:**
   - Abra: http://127.0.0.1:8000
   - Registre uma conta ou faça login
   - Comece a adicionar dados sensíveis

## 🔧 Funcionalidades

- ✅ **Criptografia Fernet** - Dados armazenados de forma segura
- ✅ **Autenticação Django** - Sistema de login/registro
- ✅ **Dashboard Protegido** - Interface para gerenciar dados
- ✅ **Armazenamento Seguro** - Dados criptografados no banco
- ✅ **Interface Responsiva** - Design moderno e intuitivo

## 🛡️ Segurança

- Criptografia AES-128 com Fernet
- Autenticação obrigatória
- CSRF protection
- Dados sensíveis nunca em texto plano

## 📁 Estrutura

```
app_seguranca/
├── manage.py
├── requirements.txt
├── settings.py
├── urls.py
├── seguranca/
│   ├── models.py
│   ├── views.py
│   └── urls.py
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── adicionar.html
    ├── login.html
    └── registrar.html
```

## 🎯 Uso

1. Faça login no sistema
2. Clique em "Adicionar Novo Dado"
3. Digite título e dados sensíveis
4. Os dados são automaticamente criptografados
5. Visualize seus dados no dashboard

---
**Desenvolvido com Django + Cryptography** 🔐
'''
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme)

def main():
    """Função principal para criar o aplicativo"""
    print("🔐 Criando App de Segurança da Informação...")
    
    # Criar estrutura de diretórios
    os.makedirs('seguranca', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Criar arquivos do Django
    criar_settings()
    criar_urls_principal()
    criar_manage()
    criar_requirements()
    criar_readme()
    criar_templates()
    
    # Criar __init__.py para o app
    with open('seguranca/__init__.py', 'w') as f:
        f.write('')
    
    # Criar models.py
    models_content = '''from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import base64

class DadosSensiveis(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    dados_criptografados = models.BinaryField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def set_dados(self, dados):
        """Criptografa e armazena dados"""
        key = Fernet.generate_key()
        cipher = Fernet(key)
        self.dados_criptografados = cipher.encrypt(dados.encode())
    
    def get_dados(self, key):
        """Descriptografa dados usando a chave"""
        cipher = Fernet(key)
        return cipher.decrypt(self.dados_criptografados).decode()
    
    class Meta:
        verbose_name = "Dado Sensível"
        verbose_name_plural = "Dados Sensíveis"
'''
    
    with open('seguranca/models.py', 'w', encoding='utf-8') as f:
        f.write(models_content)
    
    # Criar views.py
    views_content = '''from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import DadosSensiveis

@login_required
def dashboard(request):
    """Dashboard principal do aplicativo"""
    dados = DadosSensiveis.objects.filter(usuario=request.user)
    return render(request, 'dashboard.html', {
        'dados': dados,
        'usuario': request.user
    })

@login_required
def adicionar_dado(request):
    """Adiciona novo dado sensível"""
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        dados = request.POST.get('dados')
        
        if titulo and dados:
            dado = DadosSensiveis(usuario=request.user, titulo=titulo)
            dado.set_dados(dados)
            dado.save()
            return redirect('dashboard')
    
    return render(request, 'adicionar.html')

def registrar(request):
    """Registro de usuário"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'registrar.html', {'form': form})
'''
    
    with open('seguranca/views.py', 'w', encoding='utf-8') as f:
        f.write(views_content)
    
    # Criar urls.py do app
    urls_app_content = '''from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('adicionar/', views.adicionar_dado, name='adicionar_dado'),
    path('registrar/', views.registrar, name='registrar'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
'''
    
    with open('seguranca/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_app_content)
    
    print("✅ Aplicativo criado com sucesso!")
    print("\n📋 Para executar:")
    print("1. pip install -r requirements.txt")
    print("2. python manage.py makemigrations")
    print("3. python manage.py migrate")
    print("4. python manage.py runserver")
    print("5. Acesse: http://127.0.0.1:8000")

if __name__ == '__main__':
    main() 