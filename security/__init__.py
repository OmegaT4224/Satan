"""
VIOLET-AF Quantum Logic Automation System Security Framework

This package provides comprehensive security infrastructure for quantum operations,
including scanning, validation, secure logging, and encrypted state management.

Modules:
    scanner: Main security scanning engine for quantum circuit operations
    quantum_validator: Security validation for quantum circuits and operations  
    secure_logger: Secure logging with encryption and UID verification
    vault: Secure state management with encryption and access control

Usage:
    from security import SecurityScanner, QuantumValidator, SecureLogger, SecureVault
    
    # Initialize security components
    scanner = SecurityScanner()
    validator = QuantumValidator()
    logger = SecureLogger("my_app")
    vault = SecureVault("my_vault")
    
    # Perform security scan
    results = scanner.perform_full_scan()
    
    # Validate quantum circuit
    circuit = {"id": "test", "operations": ["CALL gate", "ML", "HALT"]}
    validation = validator.validate_circuit_structure(circuit)
    
    # Secure logging with UID
    uid = logger.generate_uid({"username": "user"})
    logger.log_quantum_operation("CALL gate", {}, uid)
    
    # Secure state storage
    token = vault.create_access_token(uid, ["read", "write"])
    vault.store_quantum_state("state1", {"data": "quantum_state"}, token)
"""

from .scanner import SecurityScanner
from .quantum_validator import QuantumValidator
from .secure_logger import SecureLogger, ReflectLogger
from .vault import SecureVault, AxiomDevVault

__version__ = "1.0.0"
__author__ = "VIOLET-AF Security Team"
__license__ = "Proprietary"

# Security framework metadata
SECURITY_VERSION = "1.0.0"
QUANTUM_VALIDATION_VERSION = "1.0.0"
ENCRYPTION_STANDARD = "AES-256 + RSA-2048"
COMPLIANCE_STANDARDS = ["QUANTUM_SECURITY_2024"]

__all__ = [
    "SecurityScanner",
    "QuantumValidator", 
    "SecureLogger",
    "ReflectLogger",
    "SecureVault",
    "AxiomDevVault",
    "SECURITY_VERSION",
    "QUANTUM_VALIDATION_VERSION",
    "ENCRYPTION_STANDARD",
    "COMPLIANCE_STANDARDS"
]

# Module-level configuration
DEFAULT_CONFIG = {
    "security_level": "high",
    "encryption_enabled": True,
    "logging_enabled": True,
    "validation_enabled": True,
    "monitoring_enabled": True
}

def get_security_info():
    """Get information about the security framework."""
    return {
        "version": __version__,
        "security_version": SECURITY_VERSION,
        "quantum_validation_version": QUANTUM_VALIDATION_VERSION,
        "encryption_standard": ENCRYPTION_STANDARD,
        "compliance_standards": COMPLIANCE_STANDARDS,
        "default_config": DEFAULT_CONFIG
    }

def validate_environment():
    """Validate that the security environment is properly configured."""
    import os
    
    required_vars = [
        "VAULT_PASSWORD",
        "SECURE_LOG_PASSWORD"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        import warnings
        warnings.warn(
            f"Security environment variables not set: {', '.join(missing_vars)}. "
            "This may affect security functionality.",
            UserWarning
        )
        return False
    
    return True

# Perform environment validation on import
validate_environment()