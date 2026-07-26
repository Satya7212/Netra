// static/js/pro_effects.js

// Initialize professional effects when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Add subtle hover effects to cards
    const cards = document.querySelectorAll('.pro-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Scan button loading states
    const scanButtons = document.querySelectorAll('.pro-btn');
    scanButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.classList.contains('scan-button')) {
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Scanning...';
                this.disabled = true;
                
                // Re-enable after 3 seconds (for demo)
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.disabled = false;
                }, 3000);
            }
        });
    });

    // Animate progress bars
    const progressBars = document.querySelectorAll('.pro-progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 300);
    });

    // Add subtle typing effect to terminal outputs
    const terminalOutputs = document.querySelectorAll('.terminal-output');
    terminalOutputs.forEach(terminal => {
        const originalText = terminal.innerHTML;
        terminal.innerHTML = '';
        let index = 0;
        
        function typeWriter() {
            if (index < originalText.length) {
                terminal.innerHTML += originalText.charAt(index);
                index++;
                setTimeout(typeWriter, 10);
            }
        }
        
        // Only animate if element is in viewport
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    typeWriter();
                    observer.unobserve(entry.target);
                }
            });
        });
        
        observer.observe(terminal);
    });

    // Security score animations
    const securityScores = document.querySelectorAll('.security-score');
    securityScores.forEach(score => {
        const targetScore = parseInt(score.textContent);
        let currentScore = 0;
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const timer = setInterval(() => {
                        if (currentScore < targetScore) {
                            currentScore++;
                            score.textContent = currentScore;
                        } else {
                            clearInterval(timer);
                        }
                    }, 20);
                    observer.unobserve(entry.target);
                }
            });
        });
        
        observer.observe(score);
    });
});

// Real-time system status
function updateSystemStatus() {
    const statusElement = document.getElementById('system-status');
    if (statusElement) {
        const statuses = ['Operational', 'Scanning', 'Idle'];
        const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];
        statusElement.textContent = randomStatus;
        
        // Update status color
        statusElement.className = 'scan-status ';
        if (randomStatus === 'Operational') statusElement.classList.add('status-complete');
        else if (randomStatus === 'Scanning') statusElement.classList.add('status-scanning');
        else statusElement.classList.add('status-warning');
    }
}

// Update status every 30 seconds
setInterval(updateSystemStatus, 30000);
updateSystemStatus();