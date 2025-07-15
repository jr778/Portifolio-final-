// Aguarda o carregamento completo da página
document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth scrolling para links de navegação
    const navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetSection.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Animação das barras de habilidades quando entrar na viewport
    const skillBars = document.querySelectorAll('.skill-progress');
    
    const animateSkillBars = () => {
        skillBars.forEach(bar => {
            const rect = bar.getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
            
            if (isVisible) {
                const width = bar.style.width;
                bar.style.width = '0%';
                
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
            }
        });
    };

    // Observador de interseção para animações
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Aplicar animações aos elementos
    const animatedElements = document.querySelectorAll('.project-card, .skill-item, .contact-item, .stat');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Header transparente/sólido baseado no scroll
    const header = document.querySelector('.header');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            header.style.background = 'rgba(102, 126, 234, 0.95)';
            header.style.backdropFilter = 'blur(10px)';
        } else {
            header.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            header.style.backdropFilter = 'none';
        }
    });

    // Formulário de contato
    const contactForm = document.querySelector('.contact-form form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            
            submitBtn.textContent = 'Enviando...';
            submitBtn.disabled = true;
            
            // Capturar dados do formulário
            const formData = new FormData(this);
            
            // Enviar dados via AJAX
            fetch('process_form.php', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na resposta do servidor: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    this.reset();
                } else {
                    let errorMsg = data.message;
                    if (data.debug) {
                        console.error('Debug info:', data.debug);
                        errorMsg += '\n\nDetalhes técnicos foram logados no console.';
                    }
                    alert('Erro: ' + errorMsg);
                }
            })
            .catch(error => {
                console.error('Erro completo:', error);
                alert('Erro ao enviar mensagem. Verifique o console para mais detalhes.');
            })
            .finally(() => {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            });
        });
    }

    // Efeito de hover nos cards de projeto
    const projectCards = document.querySelectorAll('.project-card');
    
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Contador animado para estatísticas
    const stats = document.querySelectorAll('.stat h3');
    
    const animateCounter = (element, target) => {
        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current) + '+';
        }, 30);
    };

    // Animar contadores quando visíveis
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.textContent);
                animateCounter(entry.target, target);
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    stats.forEach(stat => {
        statsObserver.observe(stat);
    });

    // Menu mobile (para telas pequenas)
    const createMobileMenu = () => {
        if (window.innerWidth <= 768) {
            const nav = document.querySelector('.nav');
            const navMenu = document.querySelector('.nav-menu');
            
            if (!document.querySelector('.mobile-menu-btn')) {
                const mobileBtn = document.createElement('button');
                mobileBtn.className = 'mobile-menu-btn';
                mobileBtn.innerHTML = '<i class="fas fa-bars"></i>';
                mobileBtn.style.cssText = `
                    background: none;
                    border: none;
                    color: white;
                    font-size: 1.5rem;
                    cursor: pointer;
                    display: block;
                `;
                
                nav.appendChild(mobileBtn);
                
                mobileBtn.addEventListener('click', () => {
                    navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
                });
                
                navMenu.style.cssText = `
                    display: none;
                    position: absolute;
                    top: 100%;
                    left: 0;
                    right: 0;
                    background: rgba(102, 126, 234, 0.95);
                    flex-direction: column;
                    padding: 1rem;
                    gap: 1rem;
                `;
            }
        }
    };

    // Inicializar menu mobile
    createMobileMenu();
    window.addEventListener('resize', createMobileMenu);

    // Efeito de digitação no título principal
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const text = heroTitle.innerHTML;
        heroTitle.innerHTML = '';
        
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                heroTitle.innerHTML += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };
        
        // Iniciar efeito de digitação após um delay
        setTimeout(typeWriter, 500);
    }

    // Tooltip para tecnologias
    const techTags = document.querySelectorAll('.tech-tag');
    
    techTags.forEach(tag => {
        tag.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        tag.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Scroll suave para botões
    const buttons = document.querySelectorAll('.btn[href^="#"]');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetSection.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Adicionar classe ativa ao link de navegação atual
    const sections = document.querySelectorAll('section[id]');
    const navItems = document.querySelectorAll('.nav-menu a');
    
    window.addEventListener('scroll', () => {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (window.scrollY >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });
        
        navItems.forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('href') === `#${current}`) {
                item.classList.add('active');
            }
        });
    });

    // Adicionar estilos para link ativo
    const style = document.createElement('style');
    style.textContent = `
        .nav-menu a.active {
            color: #ffd700 !important;
            font-weight: bold;
        }
    `;
    document.head.appendChild(style);

    // Rodapé móvel
    const floatingFooter = document.querySelector('.floating-footer');
    let footerVisible = false;
    let lastScrollTop = 0;
    
    // Criar botão toggle para o rodapé
    const createFooterToggle = () => {
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'footer-toggle';
        toggleBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
        document.body.appendChild(toggleBtn);
        
        toggleBtn.addEventListener('click', () => {
            if (footerVisible) {
                floatingFooter.classList.remove('show');
                toggleBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
                footerVisible = false;
            } else {
                floatingFooter.classList.add('show');
                toggleBtn.innerHTML = '<i class="fas fa-chevron-down"></i>';
                footerVisible = true;
            }
        });
    };
    
    // Mostrar rodapé ao fazer scroll para baixo
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 500) {
            // Scrolling down
            if (!footerVisible) {
                floatingFooter.classList.add('show');
                footerVisible = true;
                const toggleBtn = document.querySelector('.footer-toggle');
                if (toggleBtn) {
                    toggleBtn.innerHTML = '<i class="fas fa-chevron-down"></i>';
                }
            }
        } else if (scrollTop < lastScrollTop && scrollTop < 300) {
            // Scrolling up near top
            if (footerVisible) {
                floatingFooter.classList.remove('show');
                footerVisible = false;
                const toggleBtn = document.querySelector('.footer-toggle');
                if (toggleBtn) {
                    toggleBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
                }
            }
        }
        
        lastScrollTop = scrollTop;
    });
    
    // Esconder rodapé após 5 segundos de inatividade
    let footerTimeout;
    const hideFooterAfterDelay = () => {
        if (footerVisible) {
            footerTimeout = setTimeout(() => {
                floatingFooter.classList.remove('show');
                footerVisible = false;
                const toggleBtn = document.querySelector('.footer-toggle');
                if (toggleBtn) {
                    toggleBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
                }
            }, 5000);
        }
    };
    
    // Reset timeout quando há interação
    document.addEventListener('mousemove', () => {
        clearTimeout(footerTimeout);
        if (footerVisible) {
            hideFooterAfterDelay();
        }
    });
    
    // Inicializar rodapé móvel
    createFooterToggle();
    
    // Mostrar rodapé inicialmente após 3 segundos
    setTimeout(() => {
        floatingFooter.classList.add('show');
        footerVisible = true;
        const toggleBtn = document.querySelector('.footer-toggle');
        if (toggleBtn) {
            toggleBtn.innerHTML = '<i class="fas fa-chevron-down"></i>';
        }
        hideFooterAfterDelay();
    }, 3000);

    console.log('Portfólio carregado com sucesso! 🚀');
}); 