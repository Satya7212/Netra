# scanners/network_scanner.py

import nmap
import socket
import subprocess
import sys
from typing import Dict, List
from datetime import datetime
import json

class NetworkScanner:
    def __init__(self):
        self.nmap_available = self._check_nmap_availability()
        
    def _check_nmap_availability(self) -> bool:
        try:
            if sys.platform.startswith('win'):
                result = subprocess.run(['where', 'nmap'], capture_output=True, text=True)
            else:
                result = subprocess.run(['which', 'nmap'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

    def scan(self, target: str, scan_type: str = "standard") -> Dict:
        if self.nmap_available:
            return self._scan_with_nmap(target, scan_type)
        else:
            return self._scan_with_socket(target, scan_type)
    
    def _scan_with_nmap(self, target: str, scan_type: str) -> Dict:
        try:
            nm = nmap.PortScanner()
            
            scan_arguments = {
                "quick": "-sS -T4 --top-ports 100",
                "standard": "-sS -sV -T4 --top-ports 1000",
                "comprehensive": "-sS -sV -sC -A -T4 -p-"
            }
            
            arguments = scan_arguments.get(scan_type, scan_arguments["standard"])
            print(f"Scanning {target} with arguments: {arguments}")  # Debug
            
            # Perform the scan
            scan_result = nm.scan(target, arguments=arguments)
            
            # Return the parsed results
            return self._parse_nmap_results(nm, target)
            
        except Exception as e:
            return {"error": f"Nmap scan failed: {str(e)}"}
    
    def _parse_nmap_results(self, nm, target: str) -> Dict:
        """Parse nmap results correctly"""
        try:
            results = {
                "scan_info": {
                    "scan_type": getattr(nm, 'scaninfo', lambda: {})(),
                    "command_line": getattr(nm, 'command_line', lambda: '')() or f"nmap scan on {target}",
                    "scan_time": datetime.now().isoformat(),
                    "scan_method": "nmap"
                },
                "hosts": {}
            }
            
            if not nm.all_hosts():
                return {"error": "No hosts found or host is down"}
            
            for host in nm.all_hosts():
                host_info = {
                    "hostname": nm[host].hostname() or "Unknown",
                    "state": nm[host].state(),
                    "os_guess": self._get_os_guess(nm[host]),
                    "ports": self._get_port_info(nm[host]),
                    "vulnerability_risk": self._assess_risk(nm[host])
                }
                results["hosts"][host] = host_info
                
            return results
            
        except Exception as e:
            return {"error": f"Error parsing nmap results: {str(e)}"}
    
    def _get_os_guess(self, host_data):
        os_matches = []
        try:
            if 'osmatch' in host_data:
                for os_match in host_data['osmatch']:
                    os_matches.append({
                        'name': os_match['name'],
                        'accuracy': os_match['accuracy']
                    })
        except (KeyError, TypeError):
            pass
        return os_matches
    
    def _get_port_info(self, host_data):
        ports = []
        try:
            for protocol in host_data.all_protocols():
                port_data = host_data[protocol]
                for port, service_info in port_data.items():
                    port_info = {
                        'port': port,
                        'protocol': protocol,
                        'state': service_info['state'],
                        'service': service_info['name'],
                        'version': service_info.get('version', 'Unknown'),
                        'product': service_info.get('product', 'Unknown'),
                        'risk_level': self._assess_port_risk(port, service_info)
                    }
                    ports.append(port_info)
            return sorted(ports, key=lambda x: x['port'])
        except (KeyError, AttributeError):
            return []
    
    def _scan_with_socket(self, target: str, scan_type: str) -> Dict:
        """Fallback scanner using basic socket connections"""
        print("Nmap not found. Using basic socket scanner...")
        
        common_ports = {
            "quick": [21, 22, 23, 25, 53, 80, 110, 443, 993, 995],
            "standard": [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5900],
            "comprehensive": [21,22,23,25,53,80,110,143,443,993,995,1433,3306,3389,5432,5900,6379]
        }
        
        ports_to_scan = common_ports.get(scan_type, common_ports["standard"])
        open_ports = []
        
        for port in ports_to_scan:
            if self._check_port(target, port):
                service_info = self._guess_service(port)
                open_ports.append({
                    'port': port,
                    'state': 'open',
                    'service': service_info['name'],
                    'version': 'Unknown',
                    'product': service_info['description'],
                    'risk_level': self._assess_port_risk(port, {})
                })
        
        return {
            "scan_info": {
                "scan_type": f"socket_{scan_type}",
                "command_line": f"Basic socket scan on {target}",
                "scan_time": datetime.now().isoformat(),
                "scan_method": "socket",
                "note": "Nmap not available - using basic socket scanner"
            },
            "hosts": {
                target: {
                    "hostname": self._resolve_hostname(target),
                    "state": "up" if open_ports else "unknown",
                    "os_guess": [],
                    "ports": open_ports,
                    "vulnerability_risk": self._assess_overall_risk(open_ports)
                }
            }
        }
    
    def _check_port(self, host: str, port: int, timeout: float = 1.0) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                return result == 0
        except:
            return False
    
    def _resolve_hostname(self, ip: str) -> str:
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return "Unknown"
    
    def _guess_service(self, port: int) -> Dict:
        common_services = {
            21: {"name": "ftp", "description": "File Transfer Protocol"},
            22: {"name": "ssh", "description": "Secure Shell"},
            23: {"name": "telnet", "description": "Telnet"},
            25: {"name": "smtp", "description": "Simple Mail Transfer Protocol"},
            53: {"name": "dns", "description": "Domain Name System"},
            80: {"name": "http", "description": "Hypertext Transfer Protocol"},
            110: {"name": "pop3", "description": "Post Office Protocol v3"},
            143: {"name": "imap", "description": "Internet Message Access Protocol"},
            443: {"name": "https", "description": "HTTP Secure"},
            993: {"name": "imaps", "description": "IMAP over SSL"},
            995: {"name": "pop3s", "description": "POP3 over SSL"},
            1433: {"name": "mssql", "description": "Microsoft SQL Server"},
            3306: {"name": "mysql", "description": "MySQL Database"},
            3389: {"name": "rdp", "description": "Remote Desktop Protocol"},
            5432: {"name": "postgresql", "description": "PostgreSQL Database"},
            5900: {"name": "vnc", "description": "Virtual Network Computing"},
            6379: {"name": "redis", "description": "Redis Database"}
        }
        return common_services.get(port, {"name": "unknown", "description": "Unknown Service"})
    
    def _assess_port_risk(self, port: int, service_info: Dict) -> str:
        high_risk_ports = {21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 1433, 3306, 3389, 5432, 5900, 6379}
        return "High" if port in high_risk_ports else "Medium"
    
    def _assess_risk(self, host_data):
        try:
            open_ports = []
            high_risk_count = 0
            
            for protocol in host_data.all_protocols():
                for port, service_info in host_data[protocol].items():
                    if service_info['state'] == 'open':
                        open_ports.append(port)
                        risk = self._assess_port_risk(port, service_info)
                        if risk == "High":
                            high_risk_count += 1
            
            total_score = len(open_ports) + (high_risk_count * 2)
            
            if total_score >= 10:
                risk_level = "Critical"
            elif total_score >= 5:
                risk_level = "High"
            elif total_score >= 2:
                risk_level = "Medium"
            else:
                risk_level = "Low"
                
            return {
                "risk_level": risk_level,
                "open_ports_count": len(open_ports),
                "high_risk_ports_count": high_risk_count,
                "score": total_score
            }
        except:
            return {
                "risk_level": "Unknown",
                "open_ports_count": 0,
                "high_risk_ports_count": 0,
                "score": 0
            }
    
    def _assess_overall_risk(self, open_ports: List) -> Dict:
        high_risk_count = sum(1 for port in open_ports if port['risk_level'] == 'High')
        total_score = len(open_ports) + (high_risk_count * 2)
        
        if total_score >= 10:
            risk_level = "Critical"
        elif total_score >= 5:
            risk_level = "High"
        elif total_score >= 2:
            risk_level = "Medium"
        else:
            risk_level = "Low"
            
        return {
            "risk_level": risk_level,
            "open_ports_count": len(open_ports),
            "high_risk_ports_count": high_risk_count,
            "score": total_score
        }