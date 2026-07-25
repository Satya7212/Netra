# scanners/email_security_scanner.py

import dns.resolver
import socket
from typing import Dict, List
from datetime import datetime

class EmailSecurityScanner:
    def __init__(self):
        self.common_dkim_selectors = ['default', 'google', 'selector1', 'selector2']
    
    def analyze_domain(self, domain: str) -> Dict:
        """Comprehensive email security analysis"""
        try:
            results = {
                'domain': domain,
                'scan_time': datetime.now().isoformat(),
                'spf': self._check_spf(domain),
                'dmarc': self._check_dmarc(domain),
                'dkim': self._check_dkim(domain),
                'mx_records': self._check_mx_records(domain),
                'security_score': 0
            }
            
            results['security_score'] = self._calculate_email_security_score(results)
            results['recommendations'] = self._generate_email_recommendations(results)
            
            return results
            
        except Exception as e:
            return {'error': str(e), 'domain': domain}
    
    def _check_spf(self, domain: str) -> Dict:
        """Check SPF record configuration"""
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            for rdata in answers:
                record = str(rdata)
                if 'v=spf1' in record:
                    return {
                        'record': record,
                        'status': 'Found',
                        'analysis': self._analyze_spf_record(record)
                    }
            return {'status': 'Missing', 'risk': 'High'}
        except:
            return {'status': 'Error', 'risk': 'High'}
    
    def _analyze_spf_record(self, record: str) -> Dict:
        """Analyze SPF record for common issues"""
        issues = []
        
        if '+all' in record:
            issues.append("SPF record uses +all (too permissive)")
        elif '~all' not in record and '-all' not in record:
            issues.append("SPF record should end with ~all or -all")
        
        return {
            'issues': issues,
            'risk_level': 'High' if issues else 'Low'
        }
    
    def _check_dmarc(self, domain: str) -> Dict:
        """Check DMARC record configuration"""
        try:
            answers = dns.resolver.resolve(f'_dmarc.{domain}', 'TXT')
            for rdata in answers:
                record = str(rdata)
                if 'v=DMARC1' in record:
                    return {
                        'record': record,
                        'status': 'Found',
                        'analysis': self._analyze_dmarc_record(record)
                    }
            return {'status': 'Missing', 'risk': 'High'}
        except:
            return {'status': 'Missing', 'risk': 'High'}
    
    def _analyze_dmarc_record(self, record: str) -> Dict:
        """Analyze DMARC record for common issues"""
        issues = []
        
        if 'p=none' in record:
            issues.append("DMARC policy is set to 'none' (monitoring only)")
        if 'p=quarantine' in record:
            issues.append("DMARC policy is set to 'quarantine' (good)")
        if 'p=reject' in record:
            issues.append("DMARC policy is set to 'reject' (optimal)")
        
        return {
            'issues': issues,
            'risk_level': 'Low' if 'p=reject' in record else 'Medium'
        }
    
    def _check_dkim(self, domain: str) -> Dict:
        """Check DKIM record configuration"""
        found_selectors = []
        
        for selector in self.common_dkim_selectors:
            try:
                dns.resolver.resolve(f'{selector}._domainkey.{domain}', 'TXT')
                found_selectors.append(selector)
            except:
                continue
        
        if found_selectors:
            return {
                'status': 'Found',
                'selectors': found_selectors,
                'risk_level': 'Low'
            }
        else:
            return {
                'status': 'Missing',
                'risk_level': 'High'
            }
    
    def _check_mx_records(self, domain: str) -> Dict:
        """Check MX records configuration"""
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            mx_records = []
            for rdata in answers:
                mx_records.append({
                    'preference': rdata.preference,
                    'exchange': str(rdata.exchange)
                })
            
            return {
                'status': 'Found',
                'records': mx_records,
                'risk_level': 'Low'
            }
        except:
            return {
                'status': 'Missing',
                'risk_level': 'High'
            }
    
    def _calculate_email_security_score(self, results: Dict) -> int:
        """Calculate email security score (0-100)"""
        score = 100
        
        # SPF scoring
        spf = results.get('spf', {})
        if spf.get('status') != 'Found':
            score -= 25
        elif spf.get('analysis', {}).get('risk_level') == 'High':
            score -= 15
        
        # DMARC scoring
        dmarc = results.get('dmarc', {})
        if dmarc.get('status') != 'Found':
            score -= 25
        elif dmarc.get('analysis', {}).get('risk_level') == 'Medium':
            score -= 10
        
        # DKIM scoring
        dkim = results.get('dkim', {})
        if dkim.get('status') != 'Found':
            score -= 25
        
        # MX scoring
        mx = results.get('mx_records', {})
        if mx.get('status') != 'Found':
            score -= 25
        
        return max(score, 0)
    
    def _generate_email_recommendations(self, results: Dict) -> List[str]:
        """Generate email security recommendations"""
        recommendations = []
        
        spf = results.get('spf', {})
        if spf.get('status') != 'Found':
            recommendations.append("Add SPF record to prevent email spoofing")
        
        dmarc = results.get('dmarc', {})
        if dmarc.get('status') != 'Found':
            recommendations.append("Add DMARC record for email authentication")
        
        dkim = results.get('dkim', {})
        if dkim.get('status') != 'Found':
            recommendations.append("Configure DKIM for email signing")
        
        mx = results.get('mx_records', {})
        if mx.get('status') != 'Found':
            recommendations.append("Configure MX records for email delivery")
        
        return recommendations