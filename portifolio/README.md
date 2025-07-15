# Portfólio HTML - Básico e Moderno

Um portfólio profissional desenvolvido em HTML puro com design moderno e responsivo.

## 🚀 Características

- **Design Moderno**: Interface limpa e profissional
- **Totalmente Responsivo**: Funciona perfeitamente em desktop, tablet e mobile
- **Animações Suaves**: Efeitos visuais elegantes
- **Seções Completas**: Início, Sobre, Projetos, Habilidades e Contato
- **Formulário de Contato**: Funcional com validação
- **Navegação Suave**: Scroll automático entre seções
- **Ícones Font Awesome**: Ícones profissionais
- **Rodapé Móvel**: Footer flutuante que aparece ao fazer scroll

## 📁 Estrutura de Arquivos

```
portifolio/
├── portifolio.html   # Arquivo principal
├── style.css         # Estilos CSS
├── script.js         # JavaScript interativo
├── process_form.php  # Processamento do formulário
├── config.php        # Configurações
└── README.md         # Este arquivo
```

## 🛠️ Como Usar

### 1. Configuração Básica

1. Coloque todos os arquivos em um servidor web com PHP habilitado
2. Acesse `portifolio.html` no seu navegador
3. Configure seu email no arquivo `config.php`

### 2. Personalização

#### Informações Pessoais
Edite o arquivo `portifolio.html` e altere:

```php
// Seção Início
<h1 class="hero-title">Olá, eu sou <span class="highlight">Seu Nome</span></h1>
<p class="hero-subtitle">Desenvolvedor Web Full Stack</p>

// Seção Sobre
<p>Sou um desenvolvedor web apaixonado por tecnologia...</p>

// Estatísticas
<div class="stat">
    <h3>3+</h3>
    <p>Anos de Experiência</p>
</div>
```

#### Projetos
Edite diretamente o HTML no arquivo `portifolio.html`:

```html
<!-- Projeto -->
<div class="project-card">
    <div class="project-image">
        <img src="URL_DA_IMAGEM" alt="Nome do Projeto">
    </div>
    <div class="project-content">
        <h3 class="project-title">Nome do Projeto</h3>
        <p class="project-description">Descrição do projeto...</p>
        <div class="project-technologies">
            <span class="tech-tag">Tecnologia 1</span>
            <span class="tech-tag">Tecnologia 2</span>
        </div>
        <a href="URL_DO_PROJETO" class="btn btn-outline">Ver Projeto</a>
    </div>
</div>
```

#### Habilidades
Edite diretamente o HTML:

```html
<div class="skill-item">
    <div class="skill-info">
        <span class="skill-name">Nome da Habilidade</span>
        <span class="skill-percentage">85%</span>
    </div>
    <div class="skill-bar">
        <div class="skill-progress" style="width: 85%"></div>
    </div>
</div>
```

#### Informações de Contato
Altere as informações na seção de contato:

```html
<div class="contact-item">
    <i class="fas fa-envelope"></i>
    <div>
        <h4>Email</h4>
        <p>seu.email@exemplo.com</p>
    </div>
</div>
```

#### Configuração de Email
Para receber emails reais, edite o arquivo `config.php`:

```php
'email' => 'seu.email@exemplo.com', // ALTERE PARA SEU EMAIL REAL
```

### 3. Personalização de Cores

Edite o arquivo `style.css` para alterar as cores:

```css
/* Cores principais */
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #ffd700;
    --text-color: #333;
    --light-bg: #f8f9fa;
}
```

## 🎨 Funcionalidades

### Animações
- Efeito de digitação no título principal
- Animações de entrada para cards e elementos
- Barras de habilidades animadas
- Contadores animados para estatísticas

### Interatividade
- Navegação suave entre seções
- Menu responsivo para mobile
- Efeitos hover nos elementos
- Formulário de contato funcional
- Rodapé móvel com navegação rápida

### Responsividade
- Design adaptativo para todos os dispositivos
- Menu hambúrguer para mobile
- Grid responsivo para projetos
- Layout flexível para habilidades

## 📱 Compatibilidade

- ✅ Chrome
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

## 🔧 Requisitos

- Servidor web com PHP habilitado (para envio de emails)
- Conexão com internet (para Font Awesome CDN)

## 📝 Licença

Este projeto é de uso livre. Sinta-se à vontade para modificar e usar em seus projetos.

## 🤝 Contribuições

Sugestões e melhorias são sempre bem-vindas!

## 📞 Suporte

Se tiver dúvidas ou problemas, verifique:

1. Se todos os arquivos estão na mesma pasta
2. Se o servidor web está funcionando corretamente
3. Se o arquivo HTML está sendo acessado corretamente

---

**Desenvolvido com ❤️ em HTML** 