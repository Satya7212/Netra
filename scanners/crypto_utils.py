# scanners/crypto_utils.py
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import hashlib
from typing import Dict, Tuple

class CryptoTools:
    def __init__(self):
        self.backend = default_backend()
    
    def generate_key_from_password(self, password: str, salt: bytes = None) -> Tuple[bytes, bytes]:
        """Generate encryption key from password using PBKDF2"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def encrypt_text(self, text: str, password: str) -> Dict:
        """Encrypt text using password-based encryption"""
        try:
            key, salt = self.generate_key_from_password(password)
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(text.encode())
            
            return {
                'status': 'success',
                'encrypted_data': base64.urlsafe_b64encode(encrypted_data).decode(),
                'salt': base64.urlsafe_b64encode(salt).decode(),
                'algorithm': 'AES-256-CBC with PBKDF2'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def decrypt_text(self, encrypted_data: str, password: str, salt: str) -> Dict:
        """Decrypt text using password and salt"""
        try:
            salt_bytes = base64.urlsafe_b64decode(salt)
            key, _ = self.generate_key_from_password(password, salt_bytes)
            fernet = Fernet(key)
            
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data)
            decrypted_data = fernet.decrypt(encrypted_bytes)
            
            return {
                'status': 'success',
                'decrypted_data': decrypted_data.decode(),
                'algorithm': 'AES-256-CBC with PBKDF2'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def hash_text(self, text: str, algorithm: str = 'sha256') -> Dict:
        """Generate cryptographic hash of text"""
        try:
            if algorithm == 'md5':
                hashed = hashlib.md5(text.encode()).hexdigest()
            elif algorithm == 'sha1':
                hashed = hashlib.sha1(text.encode()).hexdigest()
            elif algorithm == 'sha256':
                hashed = hashlib.sha256(text.encode()).hexdigest()
            elif algorithm == 'sha512':
                hashed = hashlib.sha512(text.encode()).hexdigest()
            else:
                return {'status': 'error', 'message': 'Unsupported algorithm'}
            
            return {
                'status': 'success',
                'algorithm': algorithm.upper(),
                'hash': hashed,
                'length': len(hashed)
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def base64_encode(self, text: str) -> Dict:
        """Base64 encode text"""
        try:
            encoded = base64.b64encode(text.encode()).decode()
            return {'status': 'success', 'encoded': encoded}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def base64_decode(self, encoded_text: str) -> Dict:
        """Base64 decode text"""
        try:
            decoded = base64.b64decode(encoded_text).decode()
            return {'status': 'success', 'decoded': decoded}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}