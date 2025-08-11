# Secure Coding Guidelines for VIOLET-AF Quantum Logic Automation System

## Overview

This document provides secure coding guidelines specific to the VIOLET-AF quantum logic automation system. These guidelines ensure that quantum operations, state management, and system integrations are implemented securely.

## General Security Principles

### 1. Input Validation and Sanitization
- **Validate all inputs** at system boundaries
- **Sanitize quantum parameters** before processing
- **Use allowlists** for permitted operations and values
- **Reject unexpected or malformed inputs** explicitly

```python
def validate_quantum_operation(operation: str) -> bool:
    """Validate quantum operation against allowed operations."""
    allowed_operations = {'CALL', 'ML', 'HALT', 'LOAD', 'STORE'}
    op_parts = operation.split()
    
    if not op_parts:
        return False
    
    op_code = op_parts[0].upper()
    return op_code in allowed_operations
```

### 2. Error Handling and Information Disclosure
- **Never expose sensitive information** in error messages
- **Log security events** without revealing system internals
- **Use generic error messages** for user-facing responses
- **Implement proper exception handling**

```python
try:
    result = execute_quantum_operation(operation)
    return result
except QuantumExecutionError as e:
    # Log detailed error internally
    secure_logger.log_error(e, {'operation': operation}, uid)
    # Return generic error to user
    return {'error': 'Operation execution failed', 'code': 'QE001'}
```

### 3. Authentication and Authorization
- **Verify user identity** before any sensitive operations
- **Check permissions** for each resource access
- **Use secure token management**
- **Implement session timeouts**

## Quantum-Specific Security Guidelines

### 1. Quantum Circuit Validation

#### Operation Whitelisting
```python
def validate_quantum_circuit(circuit: Dict[str, Any]) -> ValidationResult:
    """Validate quantum circuit for security compliance."""
    validator = QuantumValidator()
    
    # Check circuit structure
    if not circuit.get('operations'):
        return ValidationResult(False, "Circuit must contain operations")
    
    # Validate each operation
    for operation in circuit['operations']:
        if not validate_quantum_operation(operation):
            return ValidationResult(False, f"Invalid operation: {operation}")
    
    return ValidationResult(True, "Circuit validated successfully")
```

#### Parameter Sanitization
```python
def sanitize_quantum_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize quantum parameters to prevent injection attacks."""
    sanitized = {}
    
    for key, value in params.items():
        # Check for dangerous patterns
        if isinstance(value, str):
            if any(pattern in value for pattern in ['../', '__', 'eval(', 'exec(']):
                raise SecurityError(f"Dangerous parameter detected: {key}")
            
            # Sanitize string value
            sanitized[key] = escape_special_chars(value)
        else:
            sanitized[key] = value
    
    return sanitized
```

### 2. Secure State Management

#### State Encryption
```python
class SecureQuantumState:
    """Secure quantum state with encryption."""
    
    def __init__(self, vault: SecureVault):
        self.vault = vault
        self.state_id = str(uuid.uuid4())
    
    def store_state(self, state_data: Dict[str, Any], token: str) -> bool:
        """Store quantum state securely."""
        # Validate state data
        if not self.validate_state_data(state_data):
            return False
        
        # Encrypt and store
        return self.vault.store_quantum_state(
            self.state_id, 
            state_data, 
            token, 
            encrypt_asymmetric=True
        )
    
    def validate_state_data(self, data: Dict[str, Any]) -> bool:
        """Validate quantum state data."""
        # Check data size
        if len(str(data)) > 1024 * 1024:  # 1MB limit
            return False
        
        # Check for dangerous content
        data_str = json.dumps(data)
        dangerous_patterns = ['eval', 'exec', 'import', 'subprocess']
        
        return not any(pattern in data_str.lower() for pattern in dangerous_patterns)
```

#### State Integrity Verification
```python
def verify_state_integrity(state_id: str, expected_checksum: str) -> bool:
    """Verify quantum state integrity."""
    state_data = retrieve_state(state_id)
    if not state_data:
        return False
    
    actual_checksum = hashlib.sha256(
        json.dumps(state_data, sort_keys=True).encode()
    ).hexdigest()
    
    return actual_checksum == expected_checksum
```

### 3. Secure Logging Implementation

#### Structured Security Logging
```python
def log_quantum_operation(operation: str, params: Dict[str, Any], 
                         result: Any, uid: str) -> None:
    """Log quantum operation with security context."""
    # Sanitize parameters for logging
    safe_params = sanitize_for_logging(params)
    
    # Create log entry
    log_entry = {
        'operation_type': 'quantum_execution',
        'operation': operation,
        'parameters': safe_params,
        'result_hash': hashlib.sha256(str(result).encode()).hexdigest(),
        'uid': uid,
        'timestamp': datetime.utcnow().isoformat(),
        'session_id': get_current_session_id()
    }
    
    # Log securely
    secure_logger.log_secure('quantum_operation', log_entry, uid=uid)
```

#### Log Data Sanitization
```python
def sanitize_for_logging(data: Any) -> Any:
    """Sanitize data before logging to prevent information leakage."""
    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            if any(sensitive in key.lower() for sensitive in ['password', 'secret', 'token', 'key']):
                sanitized[key] = '[REDACTED]'
            else:
                sanitized[key] = sanitize_for_logging(value)
        return sanitized
    elif isinstance(data, list):
        return [sanitize_for_logging(item) for item in data]
    elif isinstance(data, str):
        # Truncate very long strings
        return data[:100] + '...' if len(data) > 100 else data
    else:
        return data
```

## Cryptographic Guidelines

### 1. Encryption Standards

#### Symmetric Encryption
```python
from cryptography.fernet import Fernet

def create_encryption_key() -> bytes:
    """Create secure encryption key."""
    return Fernet.generate_key()

def encrypt_data(data: bytes, key: bytes) -> bytes:
    """Encrypt data using Fernet (AES-128)."""
    fernet = Fernet(key)
    return fernet.encrypt(data)

def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    """Decrypt data using Fernet."""
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data)
```

#### Asymmetric Encryption
```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def generate_key_pair():
    """Generate RSA key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key, private_key.public_key()

def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    """Encrypt data with RSA public key."""
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
```

### 2. Hashing and Integrity

#### Secure Hashing
```python
import hashlib

def create_secure_hash(data: str) -> str:
    """Create SHA-256 hash of data."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def verify_integrity(data: str, expected_hash: str) -> bool:
    """Verify data integrity using hash."""
    actual_hash = create_secure_hash(data)
    return actual_hash == expected_hash
```

#### Digital Signatures
```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def sign_data(data: bytes, private_key) -> bytes:
    """Sign data with private key."""
    return private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def verify_signature(data: bytes, signature: bytes, public_key) -> bool:
    """Verify signature with public key."""
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False
```

## Secure Integration Guidelines

### 1. EternalComputationEngine Security

#### Secure Operation Execution
```python
class SecureEternalComputationEngine(EternalComputationEngine):
    """Secure version of EternalComputationEngine."""
    
    def __init__(self):
        super().__init__()
        self.security_validator = QuantumValidator()
        self.secure_logger = SecureLogger("ece_secure")
        self.access_token = None
    
    def authenticate(self, token: str) -> bool:
        """Authenticate before operations."""
        # Verify token with vault
        if vault.verify_access(token, 'execute'):
            self.access_token = token
            return True
        return False
    
    def step(self):
        """Secure step execution with validation."""
        if not self.access_token:
            raise SecurityError("Authentication required")
        
        if self.pc >= len(self.instructions):
            self.state = "HALT"
            return
        
        inst = self.instructions[self.pc]
        
        # Validate instruction before execution
        if not self.security_validator.validate_quantum_operation(inst):
            self.secure_logger.log_security_event(
                'invalid_operation_blocked',
                {'instruction': inst, 'pc': self.pc}
            )
            self.state = "ERROR"
            return
        
        # Execute with logging
        opcode, *args = inst.split()
        self.secure_logger.log_quantum_operation(opcode, args, None, self.access_token)
        
        getattr(self, f'op_{opcode}', self.op_UNKNOWN)(*args)
        self.pc += 1
```

### 2. GitHubAgent Security

#### Secure API Integration
```python
class SecureGitHubAgent:
    """Secure GitHub integration with token protection."""
    
    def __init__(self):
        self.api_token = self.get_secure_token()
        self.secure_logger = SecureLogger("github_agent")
    
    def get_secure_token(self) -> str:
        """Retrieve GitHub token securely."""
        # Use environment variable or secure vault
        token = os.environ.get('GITHUB_TOKEN')
        if not token:
            raise SecurityError("GitHub token not configured")
        
        # Validate token format
        if not token.startswith('ghp_') and not token.startswith('github_pat_'):
            raise SecurityError("Invalid GitHub token format")
        
        return token
    
    def make_api_request(self, endpoint: str, method: str = 'GET', 
                        data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make secure API request to GitHub."""
        # Validate endpoint
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        
        # Log API access
        self.secure_logger.log_secure('github_api_request', {
            'endpoint': endpoint,
            'method': method,
            'has_data': data is not None
        })
        
        # Make request with proper headers
        headers = {
            'Authorization': f'token {self.api_token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'VIOLET-AF-QuantumSystem/1.0'
        }
        
        # Implementation would include actual HTTP request
        # with proper error handling and rate limiting
        pass
```

## Code Review Checklist

### Security Review Points
- [ ] Input validation implemented for all external inputs
- [ ] Authentication and authorization checks in place
- [ ] Sensitive data properly encrypted
- [ ] Error handling doesn't leak information
- [ ] Logging includes security-relevant events
- [ ] No hardcoded secrets or credentials
- [ ] Proper exception handling implemented
- [ ] Resource limits and timeouts configured
- [ ] SQL injection prevention (if applicable)
- [ ] Cross-site scripting prevention (if applicable)

### Quantum-Specific Review Points
- [ ] Quantum operations validated before execution
- [ ] State data encrypted and integrity-protected
- [ ] Circuit complexity limits enforced
- [ ] Dangerous operations blocked or restricted
- [ ] Quantum parameters sanitized
- [ ] State transitions logged and auditable

## Testing Guidelines

### Security Testing
```python
def test_quantum_operation_validation():
    """Test quantum operation security validation."""
    validator = QuantumValidator()
    
    # Test allowed operation
    result = validator.validate_quantum_operation("CALL test_module")
    assert result.is_valid
    
    # Test forbidden operation
    result = validator.validate_quantum_operation("EXEC malicious_code")
    assert not result.is_valid
    assert any(v['type'] == 'disallowed_operation' for v in result.violations)

def test_parameter_sanitization():
    """Test parameter sanitization."""
    dangerous_params = {
        'file_path': '../../../etc/passwd',
        'code': 'eval("malicious_code")',
        'normal_param': 'safe_value'
    }
    
    with pytest.raises(SecurityError):
        sanitize_quantum_parameters(dangerous_params)
```

### Integration Testing
```python
def test_secure_state_management():
    """Test secure quantum state storage and retrieval."""
    vault = SecureVault()
    token = vault.create_access_token('test_user', ['read', 'write'])
    
    # Store state
    state_data = {'amplitude': [0.5, 0.5], 'phase': [0, 3.14]}
    success = vault.store_quantum_state('test_state', state_data, token)
    assert success
    
    # Retrieve state
    retrieved_data = vault.retrieve_quantum_state('test_state', token)
    assert retrieved_data == state_data
    
    # Test unauthorized access
    invalid_token = 'invalid_token'
    unauthorized_data = vault.retrieve_quantum_state('test_state', invalid_token)
    assert unauthorized_data is None
```

## Deployment Security

### Environment Configuration
```python
def validate_deployment_security():
    """Validate security configuration before deployment."""
    required_env_vars = [
        'VAULT_PASSWORD',
        'SECURE_LOG_PASSWORD',
        'GITHUB_TOKEN'
    ]
    
    for var in required_env_vars:
        if not os.environ.get(var):
            raise SecurityError(f"Required environment variable {var} not set")
    
    # Validate file permissions
    sensitive_files = [
        'security/vault.py',
        'security/secure_logger.py',
        'config/security_config.yaml'
    ]
    
    for file_path in sensitive_files:
        if os.path.exists(file_path):
            stat_info = os.stat(file_path)
            if stat_info.st_mode & 0o077:  # Check if group/other have access
                raise SecurityError(f"File {file_path} has insecure permissions")
```

### Runtime Security Checks
```python
def perform_runtime_security_checks():
    """Perform security checks at runtime."""
    # Check for debug mode
    if os.environ.get('DEBUG', '').lower() == 'true':
        logging.warning("Application running in debug mode - security risk")
    
    # Check file system permissions
    validate_file_permissions()
    
    # Check network configuration
    validate_network_security()
    
    # Check logging configuration
    validate_logging_security()
```

---

*These guidelines should be followed for all development work on the VIOLET-AF quantum logic automation system. Regular security reviews and updates to these guidelines are essential for maintaining system security.*