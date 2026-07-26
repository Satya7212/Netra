// static/js/cyber_effects.js
document.addEventListener('DOMContentLoaded', function() {
    // Typing effect for terminal elements
    const terminalElements = document.querySelectorAll('.terminal-command');
    terminalElements.forEach(element => {
        const text = element.textContent;
        element.textContent = '';
        let i = 0;
        const timer = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(timer);
            }
        }, 50);
    });

    // Particle background effect
    createParticles();

    // Scan animation for cards
    const scanCards = document.querySelectorAll('.elite-card');
    scanCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 0 30px rgba(0, 255, 65, 0.4)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.boxShadow = '0 0 20px rgba(0, 255, 65, 0.3)';
        });
    });

    // Real-time clock
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
        
        const clockElement = document.getElementById('cyber-clock');
        if (clockElement) {
            clockElement.innerHTML = `<i class="fas fa-clock"></i> ${dateString} | ${timeString}`;
        }
    }
    
    setInterval(updateClock, 1000);
    updateClock();

    // Scan progress simulation
    function simulateScanProgress() {
        const progressBars = document.querySelectorAll('.cyber-progress-bar');
        progressBars.forEach(bar => {
            const currentWidth = parseInt(bar.style.width) || 0;
            if (currentWidth < 100) {
                bar.style.width = Math.min(currentWidth + Math.random() * 10, 100) + '%';
            }
        });
    }
    
    setInterval(simulateScanProgress, 500);
});

function createParticles() {
    const container = document.querySelector('.cyber-background');
    if (!container) return;
    
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'absolute';
        particle.style.width = '2px';
        particle.style.height = '2px';
        particle.style.background = 'var(--cyber-primary)';
        particle.style.borderRadius = '50%';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.opacity = Math.random() * 0.5;
        particle.style.animation = `float ${5 + Math.random() * 10}s linear infinite`;
        
        const keyframes = `
            @keyframes float {
                0% { transform: translate(0, 0) rotate(0deg); opacity: ${Math.random() * 0.5}; }
                50% { transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) rotate(180deg); opacity: ${Math.random() * 0.8}; }
                100% { transform: translate(0, 0) rotate(360deg); opacity: ${Math.random() * 0.5}; }
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = keyframes;
        document.head.appendChild(styleSheet);
        
        container.appendChild(particle);
    }
}

// Form validation enhancement
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = this.querySelectorAll('input[required]');
            let valid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    input.style.borderColor = '#ff006e';
                    input.style.boxShadow = '0 0 10px rgba(255, 0, 110, 0.3)';
                } else {
                    input.style.borderColor = 'var(--cyber-primary)';
                    input.style.boxShadow = '0 0 10px rgba(0, 255, 65, 0.3)';
                }
            });
            
            if (!valid) {
                e.preventDefault();
                // Show error message
                const errorDiv = document.createElement('div');
                errorDiv.className = 'cyber-alert';
                errorDiv.innerHTML = `
                    <div class="alert-content">
                        <i class="fas fa-exclamation-triangle"></i>
                        <span class="alert-text">Please fill in all required fields</span>
                    </div>
                    <div class="alert-progress"></div>
                `;
                this.prepend(errorDiv);
            }
        });
    });
});