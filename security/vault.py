"""
Secure state management vault for VIOLET-AF quantum logic automation system.
Provides encrypted storage and secure access for quantum state data.
"""

import os
import json
import base64
import hashlib
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta
import uuid
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding


class SecureVault:
    """Secure vault for quantum state management with encryption and access control."""
    
    def __init__(self, vault_id: str = None, vault_password: str = None):
        """Initialize the secure vault."""
        self.vault_id = vault_id or str(uuid.uuid4())
        self.creation_time = datetime.utcnow()
        self.access_log = []
        
        # Setup encryption
        self.symmetric_key = self._derive_key(vault_password)
        self.fernet = Fernet(self.symmetric_key)
        
        # Generate RSA key pair for additional security
        self.private_key, self.public_key = self._generate_key_pair()
        
        # Storage for encrypted data
        self.encrypted_storage = {}
        self.metadata_storage = {}
        
        # Access control
        self.access_tokens = {}
        self.permissions = {}
        
        self._log_access('vault_initialized', {
            'vault_id': self.vault_id,
            'encryption_enabled': True
        })
    
    def _derive_key(self, password: Optional[str]) -> bytes:
        """Derive encryption key from password."""
        if password is None:
            password = os.environ.get('VAULT_PASSWORD', 'default_quantum_vault_2024')
        
        # Use vault ID as salt for uniqueness
        salt = hashlib.sha256(self.vault_id.encode()).digest()[:16]
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def _generate_key_pair(self) -> tuple:
        """Generate RSA key pair for asymmetric encryption."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    def _log_access(self, operation: str, details: Dict[str, Any]) -> None:
        """Log vault access operations."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'operation': operation,
            'details': details,
            'session_id': str(uuid.uuid4())
        }
        self.access_log.append(log_entry)
    
    def create_access_token(self, uid: str, permissions: List[str], 
                           expires_in_hours: int = 24) -> str:
        """Create an access token for a user."""
        token = str(uuid.uuid4())
        expiry = datetime.utcnow() + timedelta(hours=expires_in_hours)
        
        self.access_tokens[token] = {
            'uid': uid,
            'permissions': permissions,
            'created_at': datetime.utcnow().isoformat(),
            'expires_at': expiry.isoformat(),
            'active': True
        }
        
        self.permissions[uid] = {
            'token': token,
            'permissions': permissions,
            'last_access': datetime.utcnow().isoformat()
        }
        
        self._log_access('token_created', {
            'uid': uid,
            'token': token[:8] + '...',  # Log partial token for security
            'permissions': permissions,
            'expires_at': expiry.isoformat()
        })
        
        return token
    
    def verify_access(self, token: str, required_permission: str) -> bool:
        """Verify if a token has the required permission."""
        if token not in self.access_tokens:
            self._log_access('access_denied', {
                'reason': 'invalid_token',
                'token': token[:8] + '...' if len(token) > 8 else 'short_token'
            })
            return False
        
        token_info = self.access_tokens[token]
        
        # Check if token is active
        if not token_info.get('active', False):
            self._log_access('access_denied', {
                'reason': 'inactive_token',
                'uid': token_info.get('uid')
            })
            return False
        
        # Check if token has expired
        expiry = datetime.fromisoformat(token_info['expires_at'])
        if datetime.utcnow() > expiry:
            token_info['active'] = False
            self._log_access('access_denied', {
                'reason': 'expired_token',
                'uid': token_info.get('uid'),
                'expired_at': token_info['expires_at']
            })
            return False
        
        # Check permissions
        if required_permission not in token_info['permissions']:
            self._log_access('access_denied', {
                'reason': 'insufficient_permissions',
                'uid': token_info.get('uid'),
                'required': required_permission,
                'available': token_info['permissions']
            })
            return False
        
        # Update last access
        uid = token_info['uid']
        if uid in self.permissions:
            self.permissions[uid]['last_access'] = datetime.utcnow().isoformat()
        
        return True
    
    def store_quantum_state(self, state_id: str, state_data: Dict[str, Any], 
                           token: str, encrypt_asymmetric: bool = False) -> bool:
        """Store quantum state data securely."""
        if not self.verify_access(token, 'write'):
            return False
        
        try:
            # Serialize state data
            state_json = json.dumps(state_data, sort_keys=True)
            
            # Create metadata
            metadata = {
                'state_id': state_id,
                'size': len(state_json),
                'created_at': datetime.utcnow().isoformat(),
                'checksum': hashlib.sha256(state_json.encode()).hexdigest(),
                'encryption_type': 'asymmetric' if encrypt_asymmetric else 'symmetric',
                'version': 1
            }
            
            # Encrypt data
            if encrypt_asymmetric:
                # For large data, use hybrid encryption
                # Encrypt data with symmetric key, then encrypt symmetric key with RSA
                encrypted_data = self.fernet.encrypt(state_json.encode())
                encrypted_key = self.public_key.encrypt(
                    self.symmetric_key,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                
                final_data = {
                    'encrypted_data': base64.b64encode(encrypted_data).decode(),
                    'encrypted_key': base64.b64encode(encrypted_key).decode()
                }
                metadata['hybrid_encryption'] = True
            else:
                # Simple symmetric encryption
                encrypted_data = self.fernet.encrypt(state_json.encode())
                final_data = base64.b64encode(encrypted_data).decode()
                metadata['hybrid_encryption'] = False
            
            # Store encrypted data and metadata
            self.encrypted_storage[state_id] = final_data
            self.metadata_storage[state_id] = metadata
            
            self._log_access('state_stored', {
                'state_id': state_id,
                'size': metadata['size'],
                'encryption_type': metadata['encryption_type']
            })
            
            return True
            
        except Exception as e:
            self._log_access('store_error', {
                'state_id': state_id,
                'error': str(e)
            })
            return False
    
    def retrieve_quantum_state(self, state_id: str, token: str) -> Optional[Dict[str, Any]]:
        """Retrieve and decrypt quantum state data."""
        if not self.verify_access(token, 'read'):
            return None
        
        if state_id not in self.encrypted_storage:
            self._log_access('retrieval_failed', {
                'state_id': state_id,
                'reason': 'state_not_found'
            })
            return None
        
        try:
            encrypted_data = self.encrypted_storage[state_id]
            metadata = self.metadata_storage[state_id]
            
            # Decrypt data based on encryption type
            if metadata.get('hybrid_encryption', False):
                # Hybrid decryption
                data_dict = encrypted_data
                encrypted_key = base64.b64decode(data_dict['encrypted_key'])
                encrypted_content = base64.b64decode(data_dict['encrypted_data'])
                
                # Decrypt symmetric key with RSA
                decrypted_key = self.private_key.decrypt(
                    encrypted_key,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                
                # Decrypt data with symmetric key
                temp_fernet = Fernet(decrypted_key)
                decrypted_data = temp_fernet.decrypt(encrypted_content)
            else:
                # Simple symmetric decryption
                encrypted_content = base64.b64decode(encrypted_data)
                decrypted_data = self.fernet.decrypt(encrypted_content)
            
            # Parse JSON data
            state_data = json.loads(decrypted_data.decode())
            
            # Verify checksum
            current_checksum = hashlib.sha256(json.dumps(state_data, sort_keys=True).encode()).hexdigest()
            stored_checksum = metadata['checksum']
            
            if current_checksum != stored_checksum:
                self._log_access('integrity_violation', {
                    'state_id': state_id,
                    'expected_checksum': stored_checksum,
                    'actual_checksum': current_checksum
                })
                return None
            
            self._log_access('state_retrieved', {
                'state_id': state_id,
                'size': metadata['size']
            })
            
            return state_data
            
        except Exception as e:
            self._log_access('retrieval_error', {
                'state_id': state_id,
                'error': str(e)
            })
            return None
    
    def delete_quantum_state(self, state_id: str, token: str) -> bool:
        """Securely delete quantum state data."""
        if not self.verify_access(token, 'delete'):
            return False
        
        if state_id not in self.encrypted_storage:
            self._log_access('deletion_failed', {
                'state_id': state_id,
                'reason': 'state_not_found'
            })
            return False
        
        try:
            # Remove from storage
            del self.encrypted_storage[state_id]
            del self.metadata_storage[state_id]
            
            self._log_access('state_deleted', {
                'state_id': state_id
            })
            
            return True
            
        except Exception as e:
            self._log_access('deletion_error', {
                'state_id': state_id,
                'error': str(e)
            })
            return False
    
    def list_quantum_states(self, token: str) -> List[Dict[str, Any]]:
        """List available quantum states (metadata only)."""
        if not self.verify_access(token, 'list'):
            return []
        
        state_list = []
        for state_id, metadata in self.metadata_storage.items():
            state_info = {
                'state_id': state_id,
                'created_at': metadata['created_at'],
                'size': metadata['size'],
                'encryption_type': metadata['encryption_type'],
                'version': metadata['version']
            }
            state_list.append(state_info)
        
        self._log_access('states_listed', {
            'count': len(state_list)
        })
        
        return state_list
    
    def backup_vault(self, backup_path: str, token: str, 
                    include_keys: bool = False) -> bool:
        """Create a backup of the vault."""
        if not self.verify_access(token, 'backup'):
            return False
        
        try:
            backup_data = {
                'vault_id': self.vault_id,
                'creation_time': self.creation_time.isoformat(),
                'backup_timestamp': datetime.utcnow().isoformat(),
                'encrypted_storage': self.encrypted_storage,
                'metadata_storage': self.metadata_storage,
                'access_log': self.access_log[-100:],  # Last 100 entries
                'include_keys': include_keys
            }
            
            if include_keys:
                # Include encrypted private key
                private_pem = self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.BestAvailableEncryption(
                        self.symmetric_key[:32]  # Use part of symmetric key as password
                    )
                )
                backup_data['private_key'] = base64.b64encode(private_pem).decode()
            
            # Encrypt backup data
            backup_json = json.dumps(backup_data)
            encrypted_backup = self.fernet.encrypt(backup_json.encode())
            
            with open(backup_path, 'wb') as f:
                f.write(encrypted_backup)
            
            self._log_access('vault_backed_up', {
                'backup_path': backup_path,
                'include_keys': include_keys,
                'size': len(encrypted_backup)
            })
            
            return True
            
        except Exception as e:
            self._log_access('backup_error', {
                'backup_path': backup_path,
                'error': str(e)
            })
            return False
    
    def restore_vault(self, backup_path: str, vault_password: str = None) -> bool:
        """Restore vault from backup."""
        try:
            with open(backup_path, 'rb') as f:
                encrypted_backup = f.read()
            
            # Try to decrypt with current key, or derive new key if password provided
            if vault_password:
                temp_key = self._derive_key(vault_password)
                temp_fernet = Fernet(temp_key)
            else:
                temp_fernet = self.fernet
            
            backup_json = temp_fernet.decrypt(encrypted_backup).decode()
            backup_data = json.loads(backup_json)
            
            # Restore data
            self.vault_id = backup_data['vault_id']
            self.creation_time = datetime.fromisoformat(backup_data['creation_time'])
            self.encrypted_storage = backup_data['encrypted_storage']
            self.metadata_storage = backup_data['metadata_storage']
            
            # Restore private key if included
            if backup_data.get('include_keys', False) and 'private_key' in backup_data:
                private_pem = base64.b64decode(backup_data['private_key'])
                self.private_key = serialization.load_pem_private_key(
                    private_pem,
                    password=self.symmetric_key[:32]
                )
                self.public_key = self.private_key.public_key()
            
            self._log_access('vault_restored', {
                'backup_path': backup_path,
                'original_creation': backup_data['creation_time'],
                'backup_timestamp': backup_data['backup_timestamp']
            })
            
            return True
            
        except Exception as e:
            self._log_access('restore_error', {
                'backup_path': backup_path,
                'error': str(e)
            })
            return False
    
    def get_vault_statistics(self, token: str) -> Optional[Dict[str, Any]]:
        """Get vault usage statistics."""
        if not self.verify_access(token, 'read'):
            return None
        
        total_size = sum(metadata['size'] for metadata in self.metadata_storage.values())
        
        stats = {
            'vault_id': self.vault_id,
            'creation_time': self.creation_time.isoformat(),
            'total_states': len(self.encrypted_storage),
            'total_size_bytes': total_size,
            'active_tokens': len([t for t in self.access_tokens.values() if t.get('active', False)]),
            'access_log_entries': len(self.access_log),
            'encryption_types': {}
        }
        
        # Count encryption types
        for metadata in self.metadata_storage.values():
            enc_type = metadata['encryption_type']
            stats['encryption_types'][enc_type] = stats['encryption_types'].get(enc_type, 0) + 1
        
        return stats
    
    def revoke_token(self, token: str, admin_token: str) -> bool:
        """Revoke an access token."""
        if not self.verify_access(admin_token, 'admin'):
            return False
        
        if token in self.access_tokens:
            self.access_tokens[token]['active'] = False
            
            self._log_access('token_revoked', {
                'revoked_token': token[:8] + '...',
                'revoked_by': self.access_tokens[admin_token]['uid']
            })
            
            return True
        
        return False
    
    def cleanup_expired_tokens(self) -> int:
        """Clean up expired access tokens."""
        current_time = datetime.utcnow()
        expired_count = 0
        
        for token, token_info in self.access_tokens.items():
            expiry = datetime.fromisoformat(token_info['expires_at'])
            if current_time > expiry:
                token_info['active'] = False
                expired_count += 1
        
        if expired_count > 0:
            self._log_access('tokens_cleaned', {
                'expired_count': expired_count
            })
        
        return expired_count


class AxiomDevVault(SecureVault):
    """Specialized vault for AxiomDevCore operations."""
    
    def __init__(self, core_id: str, **kwargs):
        """Initialize AxiomDevVault for a specific core."""
        super().__init__(vault_id=f"axiom_core_{core_id}", **kwargs)
        self.core_id = core_id
        self.axiom_states = {}
        
        self._log_access('axiom_vault_initialized', {
            'core_id': core_id
        })
    
    def store_axiom_computation(self, computation_id: str, computation_data: Dict[str, Any], 
                               token: str) -> bool:
        """Store axiom computation results."""
        axiom_data = {
            'core_id': self.core_id,
            'computation_id': computation_id,
            'computation_data': computation_data,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return self.store_quantum_state(f"axiom_{computation_id}", axiom_data, token)
    
    def retrieve_axiom_computation(self, computation_id: str, token: str) -> Optional[Dict[str, Any]]:
        """Retrieve axiom computation results."""
        return self.retrieve_quantum_state(f"axiom_{computation_id}", token)