// static/js/elite_effects.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize system status
    initializeSystemStatus();
    
    // Add typing effect to terminal elements
    initializeTerminalEffects();
    
    // Add interactive card effects
    initializeCardEffects();
    
    // Initialize real-time clock
    initializeClock();
    
    // Add particle system
    initializeParticles();
});

function initializeSystemStatus() {
    // Update status indicators
    const statusDots = document.querySelectorAll('.status-dot');
    statusDots.forEach(dot => {
        setInterval(() => {
            dot.style.opacity = dot.style.opacity === '0.5' ? '1' : '0.5';
        }, 2000);
    });
}

function initializeTerminalEffects() {
    const terminals = document.querySelectorAll('.cyber-terminal');
    terminals.forEach(terminal => {
        const commands = terminal.querySelectorAll('.terminal-command');
        commands.forEach(command => {
            const originalText = command.textContent;
            command.textContent = '';
            let i = 0;
            const timer = setInterval(() => {
                if (i < originalText.length) {
                    command.textContent += originalText.charAt(i);
                    i++;
                } else {
                    clearInterval(timer);
                }
            }, 50);
        });
    });
}

function initializeCardEffects() {
    const cards = document.querySelectorAll('.elite-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
            this.style.boxShadow = '0 20px 40px rgba(37, 99, 235, 0.3)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-5px) scale(1)';
            this.style.boxShadow = '0 15px 40px rgba(37, 99, 235, 0.2)';
        });
    });
}

function initializeClock() {
    function updateClock() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', { 
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        const dateString = now.toLocaleDateString('en-US', {
            weekday: 'short',
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
        
        // You can add a clock element to your status bar if needed
        const clockElement = document.getElementById('system-clock');
        if (clockElement) {
            clockElement.innerHTML = `<i class="fas fa-clock"></i> ${dateString} | ${timeString}`;
        }
    }
    
    setInterval(updateClock, 1000);
    updateClock();
}

function initializeParticles() {
    const background = document.querySelector('.elite-background');
    if (!background) return;
    
    for (let i = 0; i < 15; i++) {
        createParticle(background);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    const size = Math.random() * 3 + 1;
    
    particle.style.position = 'absolute';
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particle.style.background = 'var(--cyber-teal)';
    particle.style.borderRadius = '50%';
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.top = `${Math.random() * 100}%`;
    particle.style.opacity = Math.random() * 0.3;
    particle.style.boxShadow = '0 0 10px var(--cyber-teal)';
    
    const animation = particle.style.animation = `float ${5 + Math.random() * 10}s linear infinite`;
    
    const styleSheet = document.createElement('style');
    styleSheet.textContent = `
        @keyframes float {
            0% { 
                transform: translate(0, 0) rotate(0deg); 
                opacity: ${Math.random() * 0.3};
            }
            50% { 
                transform: translate(${Math.random() * 200 - 100}px, ${Math.random() * 200 - 100}px) rotate(180deg); 
                opacity: ${Math.random() * 0.6};
            }
            100% { 
                transform: translate(0, 0) rotate(360deg); 
                opacity: ${Math.random() * 0.3};
            }
        }
    `;
    
    document.head.appendChild(styleSheet);
    container.appendChild(particle);
}

// Form enhancements
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> PROCESSING...';
                submitBtn.disabled = true;
            }
        });
    });
    
    // Add input focus effects
    const inputs = document.querySelectorAll('.elite-form-control');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focus-active');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focus-active');
        });
    });
});

// Scan animation simulation
function simulateScanProgress(scanType) {
    const progressElements = document.querySelectorAll('.scan-progress');
    progressElements.forEach(element => {
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 10;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
            }
            element.style.width = `${progress}%`;
            element.setAttribute('data-progress', `${Math.round(progress)}%`);
        }, 200);
    });
}