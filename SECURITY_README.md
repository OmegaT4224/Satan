# VIOLET-AF Quantum Security Framework

A comprehensive security infrastructure for quantum logic automation systems, providing encryption, validation, secure logging, and access control for quantum operations.

## 🔒 Security Features

### Core Security Modules

- **SecurityScanner**: Automated vulnerability scanning for dependencies, code, and quantum operations
- **QuantumValidator**: Security validation for quantum circuits and operations
- **SecureLogger**: Encrypted logging with UID verification and audit trails
- **SecureVault**: Encrypted quantum state management with access control

### Security Standards

- **Encryption**: AES-256 symmetric + RSA-2048 asymmetric encryption
- **Key Derivation**: PBKDF2 with SHA-256, 100,000 iterations
- **Access Control**: Token-based authentication with role-based permissions
- **Compliance**: Quantum computing security best practices

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export VAULT_PASSWORD="your_secure_vault_password"
export SECURE_LOG_PASSWORD="your_secure_log_password"
```

### 3. Run Security Demonstration

```bash
python3 demo_security.py
```

### 4. Enable Security in EternalComputationEngine

```python
from ece_memory_kernel_repl import EternalComputationEngine

# Initialize ECE
ece = EternalComputationEngine()

# Enable security features
ece.enable_security()

# Use SECURE command in REPL
# >> SECURE
# Security features enabled.
```

## 📋 Usage Examples

### Security Scanning

```python
from security import SecurityScanner

scanner = SecurityScanner()
results = scanner.perform_full_scan('.')

print(f"Total findings: {results['summary']['total_findings']}")
print(f"Critical issues: {results['summary']['severity_breakdown']['critical']}")
```

### Quantum Circuit Validation

```python
from security import QuantumValidator

validator = QuantumValidator()

circuit = {
    'id': 'my_circuit',
    'operations': ['CALL quantum_gate', 'ML', 'HALT'],
    'parameters': {'qubits': 4}
}

result = validator.validate_circuit_structure(circuit)
print(f"Valid: {result['is_valid']}, Score: {result['security_score']}/100")
```

### Secure Logging

```python
from security import SecureLogger

logger = SecureLogger("my_app")

# Generate user UID
uid = logger.generate_uid({'username': 'quantum_user'})

# Log quantum operation
logger.log_quantum_operation(
    'quantum_fourier_transform',
    {'qubits': 4, 'precision': 0.001},
    uid,
    result={'success': True}
)
```

### Secure State Management

```python
from security import SecureVault

vault = SecureVault("my_vault")

# Create access token
token = vault.create_access_token('user_id', ['read', 'write'])

# Store quantum state
state_data = {'amplitudes': [0.5, 0.5], 'phases': [0, 3.14]}
vault.store_quantum_state('state_001', state_data, token)

# Retrieve quantum state
retrieved = vault.retrieve_quantum_state('state_001', token)
```

## 🛡️ Security Architecture

### Defense in Depth

1. **Input Validation**: All quantum parameters validated before processing
2. **Operation Whitelisting**: Only approved quantum operations allowed
3. **Encrypted Storage**: All quantum states encrypted at rest
4. **Audit Logging**: All operations logged with security context
5. **Access Control**: Token-based authentication with permissions
6. **Integrity Verification**: Checksums for all stored data

### Security Workflows

- **Automated Scanning**: GitHub Actions run security scans on every commit
- **Vulnerability Detection**: Dependency and code vulnerability scanning
- **Quantum-Specific Testing**: Custom tests for quantum operation security
- **Performance Monitoring**: Security overhead monitoring and optimization

## 📁 Directory Structure

```
security/
├── __init__.py              # Security framework package
├── scanner.py               # Main security scanning engine
├── quantum_validator.py     # Quantum circuit security validation
├── secure_logger.py         # Secure logging with encryption
├── vault.py                 # Secure state management
└── policies/
    ├── SECURITY.md          # Security policy document
    └── guidelines.md        # Secure coding guidelines

config/
├── security_config.yaml    # Security configuration
└── encryption_keys.json.template  # Key management template

.github/workflows/
├── security-scan.yml       # Automated security scanning
└── quantum-test.yml        # Quantum security testing
```

## ⚙️ Configuration

### Security Configuration (config/security_config.yaml)

```yaml
security:
  quantum_validation:
    enabled: true
    max_circuit_depth: 1000
    max_operations_per_circuit: 10000
    
  encryption:
    algorithm: "fernet"
    key_derivation:
      algorithm: "pbkdf2"
      iterations: 100000
      
  logging:
    enabled: true
    level: "INFO"
    encrypt_sensitive: true
    retention_days: 90
```

### Key Management

1. Copy `config/encryption_keys.json.template` to `config/encryption_keys.json`
2. Set environment variables for key passwords
3. Run key generation to populate encrypted keys
4. Verify `.gitignore` excludes the actual keys file

## 🔍 Security Scanning

### Automated Scans

- **Dependency Scanning**: Check for vulnerable dependencies
- **Code Analysis**: Static analysis for security issues
- **Quantum Operation Analysis**: Validate quantum circuit security
- **Secret Detection**: Scan for hardcoded secrets

### Manual Scanning

```bash
# Run comprehensive security scan
python3 -c "
from security import SecurityScanner
scanner = SecurityScanner()
results = scanner.perform_full_scan('.')
scanner.export_results('security_results.json')
"
```

## 🧪 Testing

### Run Security Tests

```bash
# GitHub Actions will run these automatically
.github/workflows/security-scan.yml    # Security scanning
.github/workflows/quantum-test.yml     # Quantum security tests
```

### Manual Testing

```bash
# Test all security components
python3 demo_security.py

# Test specific components
python3 -c "from security import SecurityScanner; print('✓ Scanner OK')"
python3 -c "from security import QuantumValidator; print('✓ Validator OK')"
python3 -c "from security import SecureLogger; print('✓ Logger OK')"
python3 -c "from security import SecureVault; print('✓ Vault OK')"
```

## 📈 Monitoring and Alerting

### Security Events

- Authentication failures
- Invalid quantum operations
- Access control violations
- Data integrity failures
- Encryption/decryption errors

### Performance Metrics

- Encryption/decryption latency
- Memory usage for secure operations
- Token validation performance
- Vault storage efficiency

## 🚨 Incident Response

### Alert Levels

- **Critical**: System compromise, data breach
- **High**: Authentication bypass, dangerous operations
- **Medium**: Failed access attempts, policy violations
- **Low**: Informational security events

### Response Procedures

1. **Immediate**: Contain incident, assess impact
2. **Investigation**: Collect evidence, determine cause
3. **Recovery**: Implement fixes, restore operations
4. **Post-Incident**: Review, improve security

## 📚 Documentation

- [Security Policy](security/policies/SECURITY.md)
- [Secure Coding Guidelines](security/policies/guidelines.md)
- [API Documentation](security/__init__.py)

## 🤝 Contributing

1. Follow secure coding guidelines
2. Run security scans before submitting
3. Include security tests for new features
4. Document security implications

## 📄 License

Proprietary - VIOLET-AF Quantum Logic Automation System

---

**⚠️ Security Notice**: This framework handles sensitive quantum computation data. Always follow security best practices and never commit encryption keys or passwords to version control.