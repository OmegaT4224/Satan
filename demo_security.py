#!/usr/bin/env python3
"""
VIOLET-AF Quantum Security Demonstration

This script demonstrates the security features of the VIOLET-AF quantum logic automation system.
It shows how to use the security scanner, quantum validator, secure logger, and vault.
"""

import os
import sys
import json
from datetime import datetime

# Set up environment for demonstration
os.environ['VAULT_PASSWORD'] = 'demo_vault_password_2024'
os.environ['SECURE_LOG_PASSWORD'] = 'demo_log_password_2024'

def main():
    print("🔒 VIOLET-AF Quantum Security Framework Demonstration")
    print("=" * 60)
    
    try:
        # Import security modules
        from security import SecurityScanner, QuantumValidator, SecureLogger, SecureVault
        print("✅ Security modules imported successfully")
        
        # 1. Security Scanner Demo
        print("\n1. 🔍 Security Scanner Demonstration")
        print("-" * 40)
        
        scanner = SecurityScanner()
        print(f"Scanner ID: {scanner.scan_id}")
        
        # Run a quick scan on security directory only
        print("Running security scan on ./security/ directory...")
        results = scanner.perform_full_scan('./security/')
        
        print(f"Scan Status: {results['status']}")
        print(f"Total Findings: {results['summary']['total_findings']}")
        print(f"Severity Breakdown: {results['summary']['severity_breakdown']}")
        
        # 2. Quantum Validator Demo
        print("\n2. ⚛️ Quantum Circuit Validator Demonstration")
        print("-" * 50)
        
        validator = QuantumValidator()
        
        # Test valid quantum circuit
        valid_circuit = {
            'id': 'demo_circuit_001',
            'operations': [
                'CALL quantum_fourier_transform',
                'ML measurement_probability',
                'HALT'
            ],
            'parameters': {
                'qubits': 4,
                'precision': 0.001,
                'algorithm': 'qft'
            }
        }
        
        validation_result = validator.validate_circuit_structure(valid_circuit)
        print(f"Valid Circuit Test:")
        print(f"  ✅ Is Valid: {validation_result['is_valid']}")
        print(f"  🔒 Security Score: {validation_result['security_score']}/100")
        print(f"  ⚠️ Violations: {len(validation_result['violations'])}")
        
        # Test invalid quantum circuit
        dangerous_circuit = {
            'id': 'demo_circuit_002_dangerous',
            'operations': [
                'EXEC rm -rf /',
                'SYSTEM cat /etc/passwd', 
                'EVAL malicious_code()'
            ],
            'parameters': {
                'file_path': '../../../etc/passwd',
                'code': 'eval("dangerous_operation")'
            }
        }
        
        dangerous_result = validator.validate_circuit_structure(dangerous_circuit)
        print(f"\nDangerous Circuit Test:")
        print(f"  ❌ Is Valid: {dangerous_result['is_valid']}")
        print(f"  🔒 Security Score: {dangerous_result['security_score']}/100")
        print(f"  ⚠️ Violations: {len(dangerous_result['violations'])}")
        
        # 3. Secure Logger Demo
        print("\n3. 📝 Secure Logger Demonstration")
        print("-" * 38)
        
        logger = SecureLogger("demo_logger", log_directory="demo_logs")
        
        # Generate user UID
        user_data = {
            'username': 'demo_quantum_operator',
            'role': 'quantum_developer',
            'security_level': 'standard'
        }
        uid = logger.generate_uid(user_data)
        print(f"Generated UID: {uid}")
        
        # Log quantum operations
        operation_id = logger.log_quantum_operation(
            'quantum_fourier_transform',
            {
                'qubits': 4,
                'input_state': [0.5, 0.5, 0.5, 0.5],
                'algorithm_variant': 'optimized'
            },
            uid,
            result={
                'success': True,
                'output_state': [0.25] * 16,
                'execution_time': 0.125,
                'fidelity': 0.99
            }
        )
        print(f"Logged Quantum Operation: {operation_id}")
        
        # Log security event
        security_event_id = logger.log_security_event(
            'quantum_circuit_validation',
            {
                'circuit_id': 'demo_circuit_001',
                'validation_result': 'passed',
                'security_score': validation_result['security_score']
            },
            severity='info',
            uid=uid
        )
        print(f"Logged Security Event: {security_event_id}")
        
        # Display log statistics
        stats = logger.get_log_statistics()
        print(f"Log Statistics: {stats['total_entries']} entries, {stats['encrypted_entries']} encrypted")
        
        # 4. Secure Vault Demo
        print("\n4. 🗄️ Secure Vault Demonstration")
        print("-" * 36)
        
        vault = SecureVault("demo_vault", "demo_vault_password_2024")
        
        # Create access token
        token = vault.create_access_token(uid, ['read', 'write', 'execute'])
        print(f"Created Access Token: {token[:16]}...")
        
        # Store quantum state
        quantum_state_data = {
            'circuit_id': 'demo_circuit_001',
            'qubits': 4,
            'amplitudes': [0.25] * 16,
            'phases': [0, 1.57, 3.14, 4.71] * 4,
            'measurement_basis': 'computational',
            'metadata': {
                'creation_time': datetime.utcnow().isoformat(),
                'creator': uid,
                'algorithm': 'quantum_fourier_transform'
            }
        }
        
        storage_success = vault.store_quantum_state(
            'demo_state_001',
            quantum_state_data,
            token,
            encrypt_asymmetric=True
        )
        print(f"Quantum State Storage: {'✅ Success' if storage_success else '❌ Failed'}")
        
        # Retrieve quantum state
        retrieved_state = vault.retrieve_quantum_state('demo_state_001', token)
        if retrieved_state:
            print(f"Quantum State Retrieval: ✅ Success")
            print(f"Data Integrity: {'✅ Verified' if retrieved_state == quantum_state_data else '❌ Compromised'}")
        else:
            print(f"Quantum State Retrieval: ❌ Failed")
        
        # Display vault statistics
        vault_stats = vault.get_vault_statistics(token)
        print(f"Vault Statistics: {vault_stats['total_states']} states, {vault_stats['total_size_bytes']} bytes")
        
        # 5. EternalComputationEngine Integration Demo
        print("\n5. 🚀 EternalComputationEngine Security Integration")
        print("-" * 52)
        
        from ece_memory_kernel_repl import EternalComputationEngine
        
        ece = EternalComputationEngine()
        print("ECE initialized")
        
        # Enable security features
        ece.enable_security("demo_ece_password")
        print("Security features enabled")
        
        # Test with safe instructions
        safe_instructions = [
            'CALL quantum_gate_demo',
            'ML probability_measurement',
            'HALT'
        ]
        
        ece.load_instructions(safe_instructions)
        print("Safe instructions loaded and validated")
        
        # Test security blocking (this should raise an exception)
        try:
            dangerous_instructions = [
                'EXEC rm -rf /',
                'SYSTEM cat /etc/passwd'
            ]
            ece.load_instructions(dangerous_instructions)
            print("❌ ERROR: Dangerous instructions should have been blocked!")
        except Exception as e:
            print(f"✅ Security Protection: Dangerous instructions blocked - {str(e)[:50]}...")
        
        print("\n🎉 Security Framework Demonstration Complete!")
        print("=" * 60)
        print("Key Features Demonstrated:")
        print("  ✅ Comprehensive security scanning")
        print("  ✅ Quantum circuit validation")
        print("  ✅ Secure encrypted logging with UID verification")
        print("  ✅ Encrypted quantum state management")
        print("  ✅ Access control with token-based authentication")
        print("  ✅ Integration with existing EternalComputationEngine")
        print("  ✅ Real-time security threat detection and blocking")
        
        # Cleanup
        print("\n🧹 Cleaning up demonstration files...")
        import shutil
        if os.path.exists('demo_logs'):
            shutil.rmtree('demo_logs')
        print("Cleanup complete")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure all security dependencies are installed:")
        print("  pip install cryptography PyYAML")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Demo Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()