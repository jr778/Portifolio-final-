# Guia de Solução de Problemas - Formulário de Contato

## 🔍 Diagnóstico de Problemas

### 1. Teste Básico
Acesse `test.php` no seu navegador para verificar:
- ✅ Versão do PHP
- ✅ Função mail disponível
- ✅ Configurações de email
- ✅ Arquivos necessários

### 2. Problemas Comuns

#### ❌ "Função mail não está disponível"
**Solução:**
- Verifique se o PHP está instalado corretamente
- Configure o sendmail ou SMTP no php.ini
- Contate seu provedor de hospedagem

#### ❌ "Arquivo de configuração não encontrado"
**Solução:**
- Verifique se `config.php` existe na mesma pasta
- Verifique as permissões do arquivo (deve ser legível)

#### ❌ "Email não configurado"
**Solução:**
- Edite `config.php` e configure seu email real
- Exemplo: `'email' => 'seu.email@gmail.com'`

#### ❌ "Falha no envio do email"
**Possíveis causas:**
1. **Servidor local** - Muitos servidores locais não têm email configurado
2. **Hospedagem gratuita** - Algumas não permitem envio de emails
3. **Configuração SMTP** - Precisa de servidor SMTP configurado

### 3. Soluções por Ambiente

#### 🏠 Servidor Local (XAMPP, WAMP, etc.)
```php
// Adicione no php.ini ou configure SMTP
[mail function]
SMTP = localhost
smtp_port = 25
sendmail_from = seu@email.com
```

#### 🌐 Hospedagem Compartilhada
- Verifique se o provedor permite envio de emails
- Use SMTP do provedor se disponível
- Contate o suporte técnico

#### ☁️ Serviços de Hospedagem
- **GitHub Pages**: Não suporta PHP
- **Netlify**: Não suporta PHP
- **Vercel**: Não suporta PHP
- **Heroku**: Suporta PHP com configuração adicional

### 4. Alternativas

#### 📧 Usar Serviço de Email Externo
```php
// Exemplo com PHPMailer
require 'PHPMailer/PHPMailer.php';
$mail = new PHPMailer();
$mail->isSMTP();
$mail->Host = 'smtp.gmail.com';
$mail->SMTPAuth = true;
$mail->Username = 'seu@gmail.com';
$mail->Password = 'sua_senha';
```

#### 🔗 Usar Formulário Externo
- **Formspree**: `action="https://formspree.io/seu-email"`
- **Netlify Forms**: `data-netlify="true"`
- **Google Forms**: Integração via iframe

### 5. Teste Manual

#### Teste 1: Verificar PHP
```bash
php -v
```

#### Teste 2: Verificar Função Mail
```php
<?php
echo function_exists('mail') ? 'OK' : 'ERRO';
?>
```

#### Teste 3: Teste de Envio
```php
<?php
$result = mail('teste@exemplo.com', 'Teste', 'Mensagem de teste');
echo $result ? 'SUCESSO' : 'FALHA';
?>
```

### 6. Logs de Erro

#### Verificar Logs do PHP
```bash
tail -f /var/log/php_errors.log
```

#### Verificar Logs do Servidor
```bash
tail -f /var/log/apache2/error.log
```

### 7. Configurações Recomendadas

#### php.ini
```ini
[mail function]
SMTP = localhost
smtp_port = 25
sendmail_from = seu@email.com
sendmail_path = "/usr/sbin/sendmail -t -i"
```

#### .htaccess (se necessário)
```apache
php_value sendmail_path "/usr/sbin/sendmail -t -i"
```

### 8. Contato para Suporte

Se os problemas persistirem:
1. ✅ Execute `test.php` e anote os resultados
2. ✅ Verifique os logs de erro
3. ✅ Teste em outro servidor
4. ✅ Considere usar serviços externos

---

**Dica:** Para desenvolvimento local, considere usar serviços como Formspree ou Netlify Forms que não requerem configuração de servidor. 