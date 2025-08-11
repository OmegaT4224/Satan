#!/usr/bin/env python3
"""
VIOLET-AF Quantum Logic Integration Test Suite
Comprehensive testing of the enhanced VIOLET-AF system with security framework
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_quantum_security():
    """Test quantum security validator"""
    print("🔐 Testing Quantum Security Validator...")
    
    from security.quantum_security import create_quantum_security_validator
    
    validator = create_quantum_security_validator()
    circuit = validator.create_violet_af_circuit()
    is_valid, message = validator.validate_quantum_circuit(circuit)
    
    print(f"   ✅ Circuit validation: {is_valid}")
    print(f"   📋 Circuit ID: {circuit.circuit_id}")
    print(f"   🔒 Circuit hash: {circuit.circuit_hash[:16]}...")
    
    return is_valid

def test_andrew_authentication():
    """Test Andrew Lee Cruz authentication"""
    print("\n👤 Testing Andrew Lee Cruz Authentication...")
    
    from security.andrew_auth import create_andrew_authenticator
    
    auth = create_andrew_authenticator()
    test_uid = "ALC-ROOT-1010-1111-XCOV∞"
    is_auth, message = auth.authenticate_uid(test_uid)
    
    print(f"   ✅ Authentication: {is_auth}")
    print(f"   🎫 Clearance level: {auth.get_security_clearance_level()}")
    
    cert_valid, cert_message = auth.validate_certificate_integrity()
    print(f"   📜 Certificate: {cert_valid}")
    
    return is_auth and cert_valid

def test_axiom_dev_core():
    """Test AxiomDevCore with security"""
    print("\n⚙️ Testing AxiomDevCore Security Wrapper...")
    
    from security.axiom_security_wrapper import create_secure_axiom_core
    
    axiom_core = create_secure_axiom_core()
    status = axiom_core.get_security_status()
    
    print(f"   ✅ Security enabled: {status['security_enabled']}")
    print(f"   🔐 Authentication: {status['authentication_status']}")
    print(f"   📊 Encrypted states: {status['encrypted_states_count']}")
    
    return status['security_enabled'] and status['authentication_status']

def test_violet_launcher():
    """Test VIOLET-AF secure launcher"""
    print("\n🚀 Testing VIOLET-AF Secure Launcher...")
    
    from security.violet_secure_launcher import violet_launch
    
    success, message = violet_launch()
    
    print(f"   ✅ Launch success: {success}")
    if success:
        print(f"   🎯 Circuit launched: {message.split(': ')[-1]}")
    else:
        print(f"   ❌ Launch failed: {message}")
    
    return success

def test_violet_state_management():
    """Test VIOLET state management"""
    print("\n💾 Testing VIOLET State Management...")
    
    from violet.secure_violet_state import create_secure_violet_state
    
    state_manager = create_secure_violet_state()
    
    # Test circuit recording
    circuit_data = {
        "qubits": 3,
        "gates": 12,
        "circuit_hash": "test_hash_123",
        "status": "active"
    }
    
    success = state_manager.update_quantum_circuit("test_circuit_integration", circuit_data)
    print(f"   ✅ Circuit recording: {success}")
    
    # Test launch recording
    launch_data = {
        "circuit_id": "test_circuit_integration", 
        "success": True,
        "config": {"secure": True}
    }
    
    success = state_manager.record_launch_event(launch_data)
    print(f"   📝 Launch recording: {success}")
    
    summary = state_manager.get_state_summary()
    print(f"   📊 State summary: {summary['circuits_count']} circuits, {summary['launches_count']} launches")
    
    return success

def test_reflect_chain():
    """Test secure ReflectChain"""
    print("\n⛓️ Testing Secure ReflectChain...")
    
    from violet.reflect_chain_secure import create_secure_reflect_chain
    
    reflect_chain = create_secure_reflect_chain()
    
    # Add test entries
    entry1 = reflect_chain.add_entry("quantum_operation", {
        "operation": "circuit_execution",
        "circuit_id": "test_123",
        "success": True
    })
    
    entry2 = reflect_chain.add_entry("security_event", {
        "event_type": "authentication",
        "uid": "ALC-ROOT-1010-1111-XCOV∞",
        "result": "success"
    })
    
    print(f"   ✅ Entry 1 added: {entry1 is not None}")
    print(f"   ✅ Entry 2 added: {entry2 is not None}")
    
    # Verify integrity
    is_valid, errors = reflect_chain.verify_chain_integrity()
    print(f"   🔒 Chain integrity: {is_valid}")
    
    status = reflect_chain.get_chain_status()
    print(f"   📊 Chain length: {status['chain_length']}")
    
    return is_valid

def test_profile_validation():
    """Test profile validation"""
    print("\n📋 Testing Profile Validation...")
    
    from integration.profile_validator import create_profile_validator
    
    validator = create_profile_validator()
    summary = validator.get_profile_summary()
    
    print(f"   👤 Profile loaded: {summary['profile_loaded']}")
    print(f"   📜 Certificate loaded: {summary['certificate_loaded']}")
    print(f"   🎫 Authorization level: {summary['authorization_level']}")
    
    return summary['profile_loaded']

def test_uid_verification():
    """Test UID verification"""
    print("\n🔑 Testing UID Verification...")
    
    from integration.uid_verifier import create_uid_verifier
    
    verifier = create_uid_verifier()
    test_uid = "ALC-ROOT-1010-1111-XCOV∞"
    
    result = verifier.comprehensive_uid_verification(test_uid)
    
    print(f"   ✅ UID verification: {result.is_valid}")
    print(f"   🔒 Security level: {result.security_level.value}")
    print(f"   ❌ Errors: {len(result.error_messages)}")
    
    return result.is_valid or result.security_level.value in ['high', 'medium']

def test_quantum_trigger_system():
    """Test quantum trigger system"""
    print("\n⚡ Testing Quantum Trigger System...")
    
    from violet.quantum_trigger import create_quantum_trigger_system
    
    trigger_system = create_quantum_trigger_system()
    status = trigger_system.get_trigger_status()
    
    print(f"   ✅ System active: {status['monitoring_active']}")
    print(f"   📊 Total triggers: {status['total_triggers']}")
    
    # Test manual trigger
    success, message = trigger_system.trigger_quantum_sequence("violet_manual_launch", {"manual_command": True})
    print(f"   🎯 Manual trigger: {success}")
    
    # Stop monitoring for clean exit
    trigger_system.stop_monitoring()
    
    return status['monitoring_active'] and success

def main():
    """Run comprehensive integration tests"""
    print("🌟 VIOLET-AF Quantum Logic Integration Test Suite")
    print("=" * 60)
    
    tests = [
        ("Quantum Security", test_quantum_security),
        ("Andrew Authentication", test_andrew_authentication),
        ("AxiomDevCore Security", test_axiom_dev_core),
        ("VIOLET Launcher", test_violet_launcher),
        ("State Management", test_violet_state_management),
        ("ReflectChain", test_reflect_chain),
        ("Profile Validation", test_profile_validation),
        ("UID Verification", test_uid_verification),
        ("Quantum Triggers", test_quantum_trigger_system),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"   ❌ Test failed with error: {str(e)}")
            results[test_name] = False
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🌟 All tests passed! VIOLET-AF system is fully integrated and operational.")
        return True
    else:
        print("⚠️ Some tests failed. Review the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)