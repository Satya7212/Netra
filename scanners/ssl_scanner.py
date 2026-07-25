# scanners/ssl_scanner.py

import ssl
import socket
from datetime import datetime
from typing import Dict,List

class SSLCertificateScanner:
    def analyze_ssl_certificate(self, domain: str) -> Dict:
        """Comprehensive SSL/TLS certificate analysis"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    analysis = {
                        'domain': domain,
                        'scan_time': datetime.now().isoformat(),
                        'certificate_info': {
                            'subject': dict(x[0] for x in cert['subject']),
                            'issuer': dict(x[0] for x in cert['issuer']),
                            'valid_from': cert['notBefore'],
                            'valid_until': cert['notAfter'],
                            'days_until_expiry': self._days_until(cert['notAfter']),
                            'serial_number': cert.get('serialNumber', 'Unknown')
                        },
                        'connection_info': {
                            'protocol': ssock.version(),
                            'cipher': ssock.cipher()[0],
                            'key_size': ssock.cipher()[2] if len(ssock.cipher()) > 2 else 'Unknown'
                        },
                        'security_assessment': self._assess_security(cert, ssock.cipher())
                    }
                    
                    return analysis
        except Exception as e:
            return {'error': str(e), 'domain': domain}
    
    def _days_until(self, date_string: str) -> int:
        """Calculate days until certificate expiration"""
        try:
            expiry_date = datetime.strptime(date_string, '%b %d %H:%M:%S %Y %Z')
            now = datetime.now()
            return (expiry_date - now).days
        except:
            return -1
    
    def _assess_security(self, cert: Dict, cipher_info: tuple) -> Dict:
        """Assess SSL/TLS security level"""
        days_until_expiry = self._days_until(cert['notAfter'])
        protocol = cipher_info[1] if len(cipher_info) > 1 else 'Unknown'
        
        issues = []
        risk_level = "Low"
        
        if days_until_expiry < 0:
            issues.append("Certificate has expired")
            risk_level = "Critical"
        elif days_until_expiry < 30:
            issues.append("Certificate expires soon")
            risk_level = "High"
        elif days_until_expiry < 90:
            issues.append("Certificate will expire in less than 90 days")
            risk_level = "Medium"
        
        # Check protocol security
        if protocol in ['TLSv1', 'TLSv1.1']:
            issues.append(f"Deprecated protocol: {protocol}")
            risk_level = "High"
        elif protocol == 'SSLv3':
            issues.append(f"Insecure protocol: {protocol}")
            risk_level = "Critical"
        
        return {
            'risk_level': risk_level,
            'issues': issues,
            'recommendations': self._generate_ssl_recommendations(issues)
        }
    
    def _generate_ssl_recommendations(self, issues: List[str]) -> List[str]:
        """Generate SSL-specific recommendations"""
        recommendations = []
        
        for issue in issues:
            if "expired" in issue.lower():
                recommendations.append("Renew SSL certificate immediately")
            elif "expires soon" in issue.lower():
                recommendations.append("Renew SSL certificate before expiration")
            elif "deprecated protocol" in issue.lower():
                recommendations.append("Upgrade to TLSv1.2 or higher")
            elif "insecure protocol" in issue.lower():
                recommendations.append("Immediately disable insecure SSL protocols")
        
        if not recommendations:
            recommendations.append("SSL configuration appears secure")
        
        return recommendations