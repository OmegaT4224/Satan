"""
Secure logging with encryption for VIOLET-AF quantum logic automation system.
Provides secure logging mechanism with UID verification and encryption capabilities.
"""

import os
import json
import logging
import hashlib
import base64
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SecureLogger:
    """Secure logging system with encryption and UID verification."""
    
    def __init__(self, log_name: str = "quantum_secure", 
                 encryption_key: Optional[bytes] = None,
                 log_directory: str = "logs"):
        """Initialize the secure logger."""
        self.log_name = log_name
        self.logger_id = str(uuid.uuid4())
        self.log_directory = log_directory
        self.session_id = str(uuid.uuid4())
        
        # Ensure log directory exists
        os.makedirs(self.log_directory, exist_ok=True)
        
        # Setup encryption
        self.fernet = self._setup_encryption(encryption_key)
        
        # Setup logging
        self.logger = self._setup_logger()
        
        # Log entry tracking
        self.log_entries = []
        self.uid_registry = {}
        
        # Log session start
        self._log_session_start()
    
    def _setup_encryption(self, encryption_key: Optional[bytes]) -> Fernet:
        """Setup encryption for secure logging."""
        if encryption_key is None:
            # Generate a key from environment or create new one
            password = os.environ.get('SECURE_LOG_PASSWORD', 'default_quantum_password').encode()
            salt = b'quantum_salt_2024'  # In production, use random salt
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
        else:
            key = encryption_key
        
        return Fernet(key)
    
    def _setup_logger(self) -> logging.Logger:
        """Setup the underlying logger."""
        logger = logging.getLogger(f'SecureLogger.{self.log_name}.{self.logger_id}')
        logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Create secure log file path
        log_file = os.path.join(self.log_directory, f"{self.log_name}_{datetime.now().strftime('%Y%m%d')}.log")
        
        # File handler for encrypted logs
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler for non-sensitive logs
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Custom formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _log_session_start(self) -> None:
        """Log the start of a new logging session."""
        session_info = {
            'session_id': self.session_id,
            'logger_id': self.logger_id,
            'start_time': datetime.utcnow().isoformat(),
            'log_name': self.log_name
        }
        
        self.log_secure('session_start', session_info, severity='info')
    
    def generate_uid(self, user_data: Dict[str, Any]) -> str:
        """Generate a unique identifier for a user/entity."""
        # Create deterministic UID based on user data
        uid_data = {
            'username': user_data.get('username', 'anonymous'),
            'timestamp': datetime.utcnow().isoformat(),
            'session_id': self.session_id
        }
        
        uid_string = json.dumps(uid_data, sort_keys=True)
        uid_hash = hashlib.sha256(uid_string.encode('utf-8')).hexdigest()
        uid = f"uid_{uid_hash[:16]}"
        
        # Register UID
        self.uid_registry[uid] = {
            'created_at': datetime.utcnow().isoformat(),
            'user_data': user_data,
            'verified': True
        }
        
        self.log_secure('uid_generated', {
            'uid': uid,
            'user_data': user_data
        }, severity='info')
        
        return uid
    
    def verify_uid(self, uid: str) -> bool:
        """Verify if a UID is valid and registered."""
        if uid not in self.uid_registry:
            self.log_secure('uid_verification_failed', {
                'uid': uid,
                'reason': 'uid_not_found'
            }, severity='warning')
            return False
        
        uid_info = self.uid_registry[uid]
        if not uid_info.get('verified', False):
            self.log_secure('uid_verification_failed', {
                'uid': uid,
                'reason': 'uid_not_verified'
            }, severity='warning')
            return False
        
        return True
    
    def log_secure(self, event_type: str, data: Dict[str, Any], 
                   severity: str = 'info', uid: Optional[str] = None,
                   encrypt: bool = True) -> str:
        """Log an event securely with optional encryption."""
        # Generate entry ID
        entry_id = str(uuid.uuid4())
        
        # Verify UID if provided
        uid_verified = True
        if uid is not None:
            uid_verified = self.verify_uid(uid)
        
        # Create log entry
        log_entry = {
            'entry_id': entry_id,
            'session_id': self.session_id,
            'logger_id': self.logger_id,
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'severity': severity,
            'uid': uid,
            'uid_verified': uid_verified,
            'data': data,
            'encrypted': encrypt
        }
        
        # Encrypt sensitive data if requested
        if encrypt and 'password' in str(data).lower() or 'secret' in str(data).lower():
            try:
                encrypted_data = self.fernet.encrypt(json.dumps(data).encode('utf-8'))
                log_entry['data'] = base64.b64encode(encrypted_data).decode('utf-8')
                log_entry['encrypted'] = True
            except Exception as e:
                self.logger.error(f"Failed to encrypt log data: {e}")
                log_entry['data'] = "[ENCRYPTION_FAILED]"
        
        # Store log entry
        self.log_entries.append(log_entry)
        
        # Log to underlying logger
        log_message = f"[{event_type}] UID:{uid or 'N/A'} Verified:{uid_verified} - {data}"
        
        if severity == 'debug':
            self.logger.debug(log_message)
        elif severity == 'info':
            self.logger.info(log_message)
        elif severity == 'warning':
            self.logger.warning(log_message)
        elif severity == 'error':
            self.logger.error(log_message)
        elif severity == 'critical':
            self.logger.critical(log_message)
        else:
            self.logger.info(log_message)
        
        return entry_id
    
    def log_quantum_operation(self, operation: str, parameters: Dict[str, Any], 
                             uid: str, result: Optional[Any] = None) -> str:
        """Log a quantum operation with security context."""
        operation_data = {
            'operation': operation,
            'parameters': parameters,
            'result': result,
            'execution_context': {
                'session_id': self.session_id,
                'timestamp': datetime.utcnow().isoformat()
            }
        }
        
        return self.log_secure('quantum_operation', operation_data, 
                              severity='info', uid=uid, encrypt=True)
    
    def log_security_event(self, event_type: str, details: Dict[str, Any], 
                          severity: str = 'warning', uid: Optional[str] = None) -> str:
        """Log a security-related event."""
        security_data = {
            'security_event_type': event_type,
            'details': details,
            'threat_level': severity,
            'detection_timestamp': datetime.utcnow().isoformat()
        }
        
        return self.log_secure('security_event', security_data, 
                              severity=severity, uid=uid, encrypt=True)
    
    def log_access_attempt(self, resource: str, uid: str, 
                          success: bool, details: Optional[Dict[str, Any]] = None) -> str:
        """Log an access attempt to a resource."""
        access_data = {
            'resource': resource,
            'success': success,
            'details': details or {},
            'access_timestamp': datetime.utcnow().isoformat()
        }
        
        severity = 'info' if success else 'warning'
        return self.log_secure('access_attempt', access_data, 
                              severity=severity, uid=uid, encrypt=False)
    
    def log_error(self, error: Exception, context: Dict[str, Any], 
                  uid: Optional[str] = None) -> str:
        """Log an error with context information."""
        error_data = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'traceback': self._get_traceback_info()
        }
        
        return self.log_secure('error', error_data, 
                              severity='error', uid=uid, encrypt=False)
    
    def _get_traceback_info(self) -> str:
        """Get simplified traceback information."""
        import traceback
        return traceback.format_exc()
    
    def decrypt_log_entry(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Decrypt a log entry if it was encrypted."""
        entry = None
        for log_entry in self.log_entries:
            if log_entry['entry_id'] == entry_id:
                entry = log_entry
                break
        
        if entry is None:
            return None
        
        if entry.get('encrypted', False) and isinstance(entry['data'], str):
            try:
                encrypted_data = base64.b64decode(entry['data'].encode('utf-8'))
                decrypted_data = self.fernet.decrypt(encrypted_data)
                entry_copy = entry.copy()
                entry_copy['data'] = json.loads(decrypted_data.decode('utf-8'))
                entry_copy['encrypted'] = False
                return entry_copy
            except Exception as e:
                self.logger.error(f"Failed to decrypt log entry {entry_id}: {e}")
                return None
        
        return entry
    
    def search_logs(self, criteria: Dict[str, Any], 
                   decrypt: bool = False) -> List[Dict[str, Any]]:
        """Search log entries based on criteria."""
        results = []
        
        for entry in self.log_entries:
            match = True
            
            # Check each criterion
            for key, value in criteria.items():
                if key not in entry:
                    match = False
                    break
                
                if isinstance(value, str):
                    if value.lower() not in str(entry[key]).lower():
                        match = False
                        break
                else:
                    if entry[key] != value:
                        match = False
                        break
            
            if match:
                if decrypt and entry.get('encrypted', False):
                    decrypted_entry = self.decrypt_log_entry(entry['entry_id'])
                    if decrypted_entry:
                        results.append(decrypted_entry)
                else:
                    results.append(entry)
        
        return results
    
    def export_logs(self, output_path: str, 
                   include_encrypted: bool = False,
                   decrypt_data: bool = False) -> bool:
        """Export logs to a file."""
        try:
            export_data = {
                'session_id': self.session_id,
                'logger_id': self.logger_id,
                'export_timestamp': datetime.utcnow().isoformat(),
                'total_entries': len(self.log_entries),
                'entries': []
            }
            
            for entry in self.log_entries:
                # Skip encrypted entries if not requested
                if entry.get('encrypted', False) and not include_encrypted:
                    continue
                
                # Decrypt if requested
                if decrypt_data and entry.get('encrypted', False):
                    decrypted_entry = self.decrypt_log_entry(entry['entry_id'])
                    if decrypted_entry:
                        export_data['entries'].append(decrypted_entry)
                else:
                    export_data['entries'].append(entry)
            
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            self.log_secure('logs_exported', {
                'output_path': output_path,
                'entry_count': len(export_data['entries']),
                'include_encrypted': include_encrypted,
                'decrypt_data': decrypt_data
            }, severity='info')
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export logs: {e}")
            return False
    
    def get_log_statistics(self) -> Dict[str, Any]:
        """Get statistics about logged events."""
        stats = {
            'total_entries': len(self.log_entries),
            'session_id': self.session_id,
            'logger_id': self.logger_id,
            'uid_count': len(self.uid_registry),
            'event_types': {},
            'severity_breakdown': {},
            'encrypted_entries': 0,
            'time_range': {
                'start': None,
                'end': None
            }
        }
        
        for entry in self.log_entries:
            # Count event types
            event_type = entry.get('event_type', 'unknown')
            stats['event_types'][event_type] = stats['event_types'].get(event_type, 0) + 1
            
            # Count severity levels
            severity = entry.get('severity', 'unknown')
            stats['severity_breakdown'][severity] = stats['severity_breakdown'].get(severity, 0) + 1
            
            # Count encrypted entries
            if entry.get('encrypted', False):
                stats['encrypted_entries'] += 1
            
            # Track time range
            timestamp = entry.get('timestamp')
            if timestamp:
                if stats['time_range']['start'] is None or timestamp < stats['time_range']['start']:
                    stats['time_range']['start'] = timestamp
                if stats['time_range']['end'] is None or timestamp > stats['time_range']['end']:
                    stats['time_range']['end'] = timestamp
        
        return stats
    
    def cleanup_old_logs(self, days_to_keep: int = 30) -> int:
        """Clean up old log entries."""
        cutoff_date = datetime.utcnow().timestamp() - (days_to_keep * 24 * 3600)
        removed_count = 0
        
        original_count = len(self.log_entries)
        self.log_entries = [
            entry for entry in self.log_entries
            if datetime.fromisoformat(entry['timestamp']).timestamp() > cutoff_date
        ]
        removed_count = original_count - len(self.log_entries)
        
        if removed_count > 0:
            self.log_secure('log_cleanup', {
                'removed_entries': removed_count,
                'days_to_keep': days_to_keep,
                'remaining_entries': len(self.log_entries)
            }, severity='info')
        
        return removed_count


class ReflectLogger(SecureLogger):
    """Extended secure logger for ReflectChain operations with enhanced security."""
    
    def __init__(self, chain_id: str, **kwargs):
        """Initialize ReflectLogger for a specific chain."""
        super().__init__(log_name=f"reflect_chain_{chain_id}", **kwargs)
        self.chain_id = chain_id
        self.reflection_states = {}
        
        self.log_secure('reflect_chain_initialized', {
            'chain_id': chain_id
        }, severity='info')
    
    def log_reflection(self, reflection_id: str, state_data: Dict[str, Any], 
                      uid: str, operation: str = 'reflect') -> str:
        """Log a reflection operation with state tracking."""
        reflection_data = {
            'chain_id': self.chain_id,
            'reflection_id': reflection_id,
            'operation': operation,
            'state_data': state_data,
            'state_hash': hashlib.sha256(json.dumps(state_data, sort_keys=True).encode()).hexdigest()
        }
        
        # Store reflection state
        self.reflection_states[reflection_id] = {
            'timestamp': datetime.utcnow().isoformat(),
            'state_data': state_data,
            'uid': uid
        }
        
        return self.log_secure('reflection_operation', reflection_data, 
                              severity='info', uid=uid, encrypt=True)
    
    def verify_reflection_chain(self, reflection_ids: List[str]) -> Dict[str, Any]:
        """Verify the integrity of a reflection chain."""
        verification_result = {
            'chain_id': self.chain_id,
            'verification_timestamp': datetime.utcnow().isoformat(),
            'reflections_verified': 0,
            'reflections_missing': [],
            'integrity_issues': [],
            'chain_valid': True
        }
        
        for reflection_id in reflection_ids:
            if reflection_id in self.reflection_states:
                verification_result['reflections_verified'] += 1
            else:
                verification_result['reflections_missing'].append(reflection_id)
                verification_result['chain_valid'] = False
        
        self.log_secure('chain_verification', verification_result, severity='info')
        return verification_result