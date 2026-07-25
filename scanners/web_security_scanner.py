# scanners/web_security_scanner.py

import requests
import ssl
import socket
from urllib.parse import urlparse
from typing import Dict, List
from datetime import datetime

class WebSecurityScanner:
    def __init__(self):
        self.critical_headers = [
            'Content-Security-Policy',
            'Strict-Transport-Security', 
            'X-Frame-Options',
            'X-Content-Type-Options',
            'Referrer-Policy'
        ]
        
        self.recommended_headers = [
            'Permissions-Policy',
            'X-XSS-Protection',
            'Cache-Control'
        ]
    
    def scan_website(self, url: str) -> Dict:
        """Comprehensive web security analysis"""
        try:
            # Ensure URL has scheme
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            results = {
                'url': url,
                'domain': domain,
                'scan_time': datetime.now().isoformat(),
                'security_headers': {},
                'ssl_info': {},
                'security_score': 0,
                'recommendations': []
            }
            
            # Check HTTPS
            results['https_redirect'] = self._check_https_redirect(url)
            
            # Analyze security headers
            results['security_headers'] = self._analyze_security_headers(url)
            
            # SSL/TLS analysis
            results['ssl_info'] = self._analyze_ssl_certificate(domain)
            
            # Calculate overall score
            results['security_score'] = self._calculate_security_score(results)
            results['recommendations'] = self._generate_recommendations(results)
            
            return results
            
        except Exception as e:
            return {'error': str(e), 'url': url}
    
    def _check_https_redirect(self, url: str) -> Dict:
        """Check if HTTP redirects to HTTPS"""
        http_url = url.replace('https://', 'http://')
        try:
            response = requests.get(http_url, allow_redirects=False, timeout=10)
            redirects_to_https = (
                response.status_code in [301, 302, 307, 308] and 
                'https://' in response.headers.get('Location', '')
            )
            return {
                'redirects': redirects_to_https,
                'status_code': response.status_code,
                'final_url': response.url if redirects_to_https else http_url
            }
        except:
            return {'redirects': False, 'error': 'Could not check redirect'}
    
    def _analyze_security_headers(self, url: str) -> Dict:
        """Analyze security headers"""
        try:
            response = requests.get(url, timeout=10, verify=True)
            headers = dict(response.headers)
            
            analysis = {}
            score = 100
            
            for header in self.critical_headers:
                if header in headers:
                    status = self._validate_header(header, headers[header])
                    analysis[header] = {
                        'present': True,
                        'value': headers[header],
                        'status': status
                    }
                    if status != 'optimal':
                        score -= 10
                else:
                    analysis[header] = {
                        'present': False,
                        'status': 'missing',
                        'risk': 'High'
                    }
                    score -= 15
            
            for header in self.recommended_headers:
                if header in headers:
                    analysis[header] = {
                        'present': True,
                        'value': headers[header]
                    }
                else:
                    analysis[header] = {
                        'present': False,
                        'risk': 'Medium'
                    }
                    score -= 5
            
            analysis['score'] = max(score, 0)
            return analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def _validate_header(self, header: str, value: str) -> str:
        """Validate header values against security best practices"""
        validation_rules = {
            'Strict-Transport-Security': {
                'optimal_indicators': ['max-age=31536000', 'includeSubDomains'],
                'min_age': 31536000
            },
            'Content-Security-Policy': {
                'optimal_indicators': ['default-src', 'script-src'],
                'unsafe_patterns': ["'unsafe-inline'", "'unsafe-eval'"]
            },
            'X-Frame-Options': {
                'optimal_values': ['DENY', 'SAMEORIGIN']
            }
        }
        
        rules = validation_rules.get(header, {})
        
        if 'optimal_values' in rules:
            if value in rules['optimal_values']:
                return 'optimal'
            else:
                return 'suboptimal'
        
        if 'optimal_indicators' in rules:
            if all(indicator in value for indicator in rules['optimal_indicators']):
                if 'unsafe_patterns' in rules:
                    if any(pattern in value for pattern in rules['unsafe_patterns']):
                        return 'suboptimal'
                return 'optimal'
        
        return 'suboptimal'
    
    def _analyze_ssl_certificate(self, domain: str) -> Dict:
        """Basic SSL certificate analysis"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        'valid': True,
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'valid_from': cert['notBefore'],
                        'valid_until': cert['notAfter'],
                        'protocol': ssock.version(),
                        'cipher': ssock.cipher()[0]
                    }
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def _calculate_security_score(self, results: Dict) -> int:
        """Calculate overall security score (0-100)"""
        score = 100
        
        # Deduct for missing critical headers
        headers = results.get('security_headers', {})
        for header_name, header_info in headers.items():
            if isinstance(header_info, dict) and not header_info.get('present', True):
                if header_name in self.critical_headers:
                    score -= 15
                elif header_name in self.recommended_headers:
                    score -= 5
        
        # Deduct for SSL issues
        if not results.get('ssl_info', {}).get('valid', False):
            score -= 30
        
        # Deduct for no HTTPS redirect
        if not results.get('https_redirect', {}).get('redirects', False):
            score -= 10
        
        return max(score, 0)
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable security recommendations"""
        recommendations = []
        
        # Header recommendations
        headers = results.get('security_headers', {})
        for header_name, header_info in headers.items():
            if isinstance(header_info, dict) and not header_info.get('present', True):
                if header_name in self.critical_headers:
                    recommendations.append(f"Add critical security header: {header_name}")
                elif header_name in self.recommended_headers:
                    recommendations.append(f"Consider adding security header: {header_name}")
        
        # SSL recommendations
        if not results.get('ssl_info', {}).get('valid', False):
            recommendations.append("Fix SSL/TLS certificate configuration")
        
        # HTTPS redirect recommendations
        if not results.get('https_redirect', {}).get('redirects', False):
            recommendations.append("Configure HTTP to HTTPS redirect")
        
        return recommendations