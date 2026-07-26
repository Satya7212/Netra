# app.py
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from flask import Flask, render_template, request, jsonify
    print("✓ Flask imported successfully")
except ImportError as e:
    print(f"✗ Flask import error: {e}")
    sys.exit(1)

# Import scanners
try:
    from scanners.network_scanner import NetworkScanner
    from scanners.web_security_scanner import WebSecurityScanner
    from scanners.ssl_scanner import SSLCertificateScanner
    from scanners.email_security_scanner import EmailSecurityScanner
    from scanners.crypto_utils import CryptoTools
    from scanners.stego_utils import SteganographyTools
    print("✓ All scanners imported successfully")
except ImportError as e:
    print(f"✗ Scanner import error: {e}")
    sys.exit(1)

from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Initialize scanners
scanners = {
    'network': NetworkScanner(),
    'web': WebSecurityScanner(), 
    'ssl': SSLCertificateScanner(),
    'email': EmailSecurityScanner(),
    'crypto': CryptoTools(),
    'stego': SteganographyTools()
}

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/scan/network', methods=['GET', 'POST'])
def network_scan():
    if request.method == 'POST':
        target = request.form.get('target', '').strip()
        scan_type = request.form.get('scan_type', 'standard')
        
        if not target:
            return render_template('network_scan.html', error="Please enter a target")
        
        try:
            # Use a safe test target if localhost fails
            if target in ['127.0.0.1', 'localhost']:
                results = scanners['network'].scan(target, "quick")
            else:
                results = scanners['network'].scan(target, scan_type)
            
            return render_template('network_scan.html', results=results, target=target)
        except Exception as e:
            return render_template('network_scan.html', error=f"Scan failed: {str(e)}")
    
    return render_template('network_scan.html')

@app.route('/scan/web-security', methods=['GET', 'POST'])
def web_security_scan():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        
        if not url:
            return render_template('web_security.html', error="Please enter a URL")
        
        try:
            results = scanners['web'].scan_website(url)
            return render_template('web_security.html', results=results, url=url)
        except Exception as e:
            return render_template('web_security.html', error=f"Scan failed: {str(e)}")
    
    return render_template('web_security.html')

@app.route('/scan/ssl', methods=['GET', 'POST'])
def ssl_scan():
    if request.method == 'POST':
        domain = request.form.get('domain', '').strip()
        
        if not domain:
            return render_template('ssl_scan.html', error="Please enter a domain")
        
        try:
            results = scanners['ssl'].analyze_ssl_certificate(domain)
            return render_template('ssl_scan.html', results=results, domain=domain)
        except Exception as e:
            return render_template('ssl_scan.html', error=f"Scan failed: {str(e)}")
    
    return render_template('ssl_scan.html')

@app.route('/scan/email', methods=['GET', 'POST'])
def email_scan():
    if request.method == 'POST':
        domain = request.form.get('domain', '').strip()
        
        if not domain:
            return render_template('email_scan.html', error="Please enter a domain")
        
        try:
            results = scanners['email'].analyze_domain(domain)
            return render_template('email_scan.html', results=results, domain=domain)
        except Exception as e:
            return render_template('email_scan.html', error=f"Scan failed: {str(e)}")
    
    return render_template('email_scan.html')

@app.route('/health')
def health_check():
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'scanners_available': list(scanners.keys())
    }
    return jsonify(status)

# Add these new routes to app.py

@app.route('/api/scan/status')
def scan_status():
    """API endpoint for scan status"""
    status = {
        'network_scanner': 'operational',
        'web_scanner': 'operational', 
        'ssl_scanner': 'operational',
        'email_scanner': 'operational',
        'last_scan': datetime.now().isoformat(),
        'uptime': '99.9%'
    }
    return jsonify(status)

@app.route('/scan/history')
def scan_history():
    """Display scan history"""
    # This would typically come from a database
    history = [
        {'type': 'network', 'target': 'scanme.nmap.org', 'time': '2024-01-15 14:30:00', 'status': 'completed'},
        {'type': 'web', 'target': 'example.com', 'time': '2024-01-15 14:25:00', 'status': 'completed'},
        {'type': 'ssl', 'target': 'google.com', 'time': '2024-01-15 14:20:00', 'status': 'completed'},
    ]
    return render_template('scan_history.html', history=history)

@app.route('/tools/encode')
def encoding_tools():
    """Text encoding/decoding tools"""
    return render_template('encoding_tools.html')

@app.route('/tools/hash')
def hashing_tools():
    """Hash generation tools"""
    return render_template('hashing_tools.html')

@app.route('/tools/crypto', methods=['GET', 'POST'])
def crypto_tools():
    """Cryptography tools - encryption, decryption, hashing"""
    results = None
    error = None
    
    if request.method == 'POST':
        tool_type = request.form.get('tool_type')
        
        try:
            if tool_type == 'encrypt':
                text = request.form.get('text', '')
                password = request.form.get('password', '')
                if text and password:
                    results = scanners['crypto'].encrypt_text(text, password)
                else:
                    error = "Please provide both text and password"
                    
            elif tool_type == 'decrypt':
                encrypted_data = request.form.get('encrypted_data', '')
                password = request.form.get('password', '')
                salt = request.form.get('salt', '')
                if encrypted_data and password and salt:
                    results = scanners['crypto'].decrypt_text(encrypted_data, password, salt)
                else:
                    error = "Please provide encrypted data, password, and salt"
                    
            elif tool_type == 'hash':
                text = request.form.get('text', '')
                algorithm = request.form.get('algorithm', 'sha256')
                if text:
                    results = scanners['crypto'].hash_text(text, algorithm)
                else:
                    error = "Please provide text to hash"
                    
            elif tool_type == 'base64_encode':
                text = request.form.get('text', '')
                if text:
                    results = scanners['crypto'].base64_encode(text)
                else:
                    error = "Please provide text to encode"
                    
            elif tool_type == 'base64_decode':
                encoded_text = request.form.get('encoded_text', '')
                if encoded_text:
                    results = scanners['crypto'].base64_decode(encoded_text)
                else:
                    error = "Please provide encoded text"
                    
        except Exception as e:
            error = f"Operation failed: {str(e)}"
    
    return render_template('crypto_tools.html', results=results, error=error)

@app.route('/tools/stego', methods=['GET', 'POST'])
def stego_tools():
    """Steganography tools - hide/extract text in images"""
    results = None
    error = None
    
    if request.method == 'POST':
        tool_type = request.form.get('tool_type')
        
        try:
            if 'image' in request.files:
                image_file = request.files['image']
                if image_file.filename:
                    image_data = image_file.read()
                    
                    if tool_type == 'encode':
                        text = request.form.get('text', '')
                        password = request.form.get('password', '')
                        if text:
                            results = scanners['stego'].encode_text_in_image(image_data, text, password)
                        else:
                            error = "Please provide text to hide"
                            
                    elif tool_type == 'decode':
                        results = scanners['stego'].decode_text_from_image(image_data)
                        
                    elif tool_type == 'analyze':
                        results = scanners['stego'].analyze_image_stego(image_data)
                else:
                    error = "Please select an image file"
            else:
                error = "Please select an image file"
                
        except Exception as e:
            error = f"Operation failed: {str(e)}"
    
    return render_template('stego_tools.html', results=results, error=error)

if __name__ == '__main__':
    print("🚀 Starting Cybersecurity Dashboard...")
    print("📊 Available scanners:", list(scanners.keys()))
    print("🌐 Access the dashboard at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)