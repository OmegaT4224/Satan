"""
Quantum circuit security validation for VIOLET-AF quantum logic automation system.
Validates quantum circuit structure, operations, and state management for security.
"""

import hashlib
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import uuid
import re


class QuantumValidator:
    """Security validator for quantum circuits and operations."""
    
    def __init__(self, security_config: Optional[Dict[str, Any]] = None):
        """Initialize the quantum validator."""
        self.validator_id = str(uuid.uuid4())
        self.config = security_config or self._default_config()
        self.logger = self._setup_logger()
        self.validation_cache = {}
        
    def _default_config(self) -> Dict[str, Any]:
        """Default security configuration for quantum validation."""
        return {
            'max_circuit_depth': 1000,
            'max_operations_per_circuit': 10000,
            'allowed_operations': [
                'CALL', 'ML', 'HALT', 'LOAD', 'STORE', 
                'ADD', 'SUB', 'MUL', 'DIV', 'QUANTUM_GATE'
            ],
            'forbidden_operations': [
                'EXEC', 'SYSTEM', 'SHELL', 'EVAL', 'IMPORT'
            ],
            'validate_parameters': True,
            'require_signature': False,
            'enable_state_encryption': True
        }
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for quantum validator."""
        logger = logging.getLogger(f'QuantumValidator.{self.validator_id}')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def validate_circuit_structure(self, circuit: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the structure of a quantum circuit."""
        validation_result = {
            'circuit_id': circuit.get('id', 'unknown'),
            'validator_id': self.validator_id,
            'timestamp': datetime.utcnow().isoformat(),
            'is_valid': True,
            'violations': [],
            'warnings': [],
            'security_score': 100
        }
        
        try:
            # Validate basic structure
            self._validate_basic_structure(circuit, validation_result)
            
            # Validate operations
            if 'operations' in circuit:
                self._validate_operations(circuit['operations'], validation_result)
            
            # Validate parameters
            if 'parameters' in circuit:
                self._validate_parameters(circuit['parameters'], validation_result)
            
            # Validate circuit depth and complexity
            self._validate_complexity(circuit, validation_result)
            
            # Calculate final security score
            validation_result['security_score'] = self._calculate_security_score(validation_result)
            
        except Exception as e:
            self.logger.error(f"Circuit validation failed: {e}")
            validation_result['is_valid'] = False
            validation_result['violations'].append({
                'type': 'validation_error',
                'severity': 'critical',
                'description': f"Validation process failed: {e}",
                'timestamp': datetime.utcnow().isoformat()
            })
        
        return validation_result
    
    def _validate_basic_structure(self, circuit: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Validate basic circuit structure requirements."""
        required_fields = ['id', 'operations']
        
        for field in required_fields:
            if field not in circuit:
                result['violations'].append({
                    'type': 'missing_required_field',
                    'severity': 'high',
                    'field': field,
                    'description': f"Required field '{field}' is missing from circuit",
                    'timestamp': datetime.utcnow().isoformat()
                })
                result['is_valid'] = False
        
        # Validate circuit ID format
        if 'id' in circuit:
            circuit_id = circuit['id']
            if not isinstance(circuit_id, str) or len(circuit_id) == 0:
                result['violations'].append({
                    'type': 'invalid_circuit_id',
                    'severity': 'medium',
                    'description': "Circuit ID must be a non-empty string",
                    'timestamp': datetime.utcnow().isoformat()
                })
    
    def _validate_operations(self, operations: List[Any], result: Dict[str, Any]) -> None:
        """Validate quantum operations in the circuit."""
        if not isinstance(operations, list):
            result['violations'].append({
                'type': 'invalid_operations_format',
                'severity': 'high',
                'description': "Operations must be a list",
                'timestamp': datetime.utcnow().isoformat()
            })
            result['is_valid'] = False
            return
        
        # Check operation count
        if len(operations) > self.config['max_operations_per_circuit']:
            result['violations'].append({
                'type': 'too_many_operations',
                'severity': 'high',
                'count': len(operations),
                'max_allowed': self.config['max_operations_per_circuit'],
                'description': f"Circuit exceeds maximum operation count of {self.config['max_operations_per_circuit']}",
                'timestamp': datetime.utcnow().isoformat()
            })
            result['is_valid'] = False
        
        # Validate individual operations
        for i, operation in enumerate(operations):
            self._validate_single_operation(operation, i, result)
    
    def _validate_single_operation(self, operation: Any, index: int, result: Dict[str, Any]) -> None:
        """Validate a single quantum operation."""
        if isinstance(operation, str):
            # Parse operation string
            parts = operation.split()
            if parts:
                op_code = parts[0].upper()
                op_args = parts[1:] if len(parts) > 1 else []
                
                # Check if operation is allowed
                if op_code not in self.config['allowed_operations']:
                    severity = 'critical' if op_code in self.config['forbidden_operations'] else 'medium'
                    result['violations'].append({
                        'type': 'disallowed_operation',
                        'severity': severity,
                        'operation': op_code,
                        'index': index,
                        'description': f"Operation '{op_code}' is not in allowed operations list",
                        'timestamp': datetime.utcnow().isoformat()
                    })
                    if severity == 'critical':
                        result['is_valid'] = False
                
                # Validate operation arguments
                self._validate_operation_args(op_code, op_args, index, result)
        
        elif isinstance(operation, dict):
            # Validate structured operation
            self._validate_structured_operation(operation, index, result)
        
        else:
            result['violations'].append({
                'type': 'invalid_operation_format',
                'severity': 'medium',
                'index': index,
                'description': f"Operation at index {index} has invalid format",
                'timestamp': datetime.utcnow().isoformat()
            })
    
    def _validate_operation_args(self, op_code: str, args: List[str], index: int, result: Dict[str, Any]) -> None:
        """Validate arguments for specific operations."""
        arg_validation_rules = {
            'CALL': {'min_args': 1, 'max_args': 3},
            'LOAD': {'min_args': 1, 'max_args': 2},
            'STORE': {'min_args': 2, 'max_args': 2},
            'ADD': {'min_args': 2, 'max_args': 3},
            'SUB': {'min_args': 2, 'max_args': 3},
            'MUL': {'min_args': 2, 'max_args': 3},
            'DIV': {'min_args': 2, 'max_args': 3},
        }
        
        if op_code in arg_validation_rules:
            rules = arg_validation_rules[op_code]
            arg_count = len(args)
            
            if arg_count < rules['min_args']:
                result['violations'].append({
                    'type': 'insufficient_arguments',
                    'severity': 'high',
                    'operation': op_code,
                    'index': index,
                    'expected_min': rules['min_args'],
                    'actual': arg_count,
                    'description': f"Operation '{op_code}' requires at least {rules['min_args']} arguments",
                    'timestamp': datetime.utcnow().isoformat()
                })
            
            elif arg_count > rules['max_args']:
                result['violations'].append({
                    'type': 'too_many_arguments',
                    'severity': 'medium',
                    'operation': op_code,
                    'index': index,
                    'expected_max': rules['max_args'],
                    'actual': arg_count,
                    'description': f"Operation '{op_code}' accepts at most {rules['max_args']} arguments",
                    'timestamp': datetime.utcnow().isoformat()
                })
        
        # Check for dangerous argument patterns
        for arg in args:
            if self._is_dangerous_argument(arg):
                result['violations'].append({
                    'type': 'dangerous_argument',
                    'severity': 'high',
                    'operation': op_code,
                    'argument': arg,
                    'index': index,
                    'description': f"Potentially dangerous argument detected: {arg}",
                    'timestamp': datetime.utcnow().isoformat()
                })
    
    def _is_dangerous_argument(self, arg: str) -> bool:
        """Check if an argument contains dangerous patterns."""
        dangerous_patterns = [
            r'\.\./',           # Directory traversal
            r'__.*__',          # Python dunder methods
            r'eval\s*\(',       # Eval calls
            r'exec\s*\(',       # Exec calls
            r'import\s+',       # Import statements
            r'subprocess',      # Subprocess calls
            r'os\.system',      # OS system calls
            r'open\s*\(',       # File operations
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, arg, re.IGNORECASE):
                return True
        
        return False
    
    def _validate_structured_operation(self, operation: Dict[str, Any], index: int, result: Dict[str, Any]) -> None:
        """Validate a structured operation dictionary."""
        required_fields = ['type']
        
        for field in required_fields:
            if field not in operation:
                result['violations'].append({
                    'type': 'missing_operation_field',
                    'severity': 'medium',
                    'field': field,
                    'index': index,
                    'description': f"Operation at index {index} missing required field '{field}'",
                    'timestamp': datetime.utcnow().isoformat()
                })
    
    def _validate_parameters(self, parameters: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Validate circuit parameters."""
        if not isinstance(parameters, dict):
            result['violations'].append({
                'type': 'invalid_parameters_format',
                'severity': 'medium',
                'description': "Parameters must be a dictionary",
                'timestamp': datetime.utcnow().isoformat()
            })
            return
        
        # Validate parameter values
        for key, value in parameters.items():
            if self._is_dangerous_parameter(key, value):
                result['violations'].append({
                    'type': 'dangerous_parameter',
                    'severity': 'high',
                    'parameter': key,
                    'description': f"Parameter '{key}' contains potentially dangerous value",
                    'timestamp': datetime.utcnow().isoformat()
                })
    
    def _is_dangerous_parameter(self, key: str, value: Any) -> bool:
        """Check if a parameter is potentially dangerous."""
        dangerous_keys = ['password', 'secret', 'token', 'key', 'auth']
        
        # Check for sensitive parameter names
        for danger_key in dangerous_keys:
            if danger_key in key.lower():
                return True
        
        # Check for dangerous values
        if isinstance(value, str):
            return self._is_dangerous_argument(value)
        
        return False
    
    def _validate_complexity(self, circuit: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Validate circuit complexity and resource usage."""
        operations = circuit.get('operations', [])
        
        # Calculate circuit depth (simplified)
        circuit_depth = len(operations)  # Simplified depth calculation
        
        if circuit_depth > self.config['max_circuit_depth']:
            result['violations'].append({
                'type': 'circuit_too_deep',
                'severity': 'medium',
                'depth': circuit_depth,
                'max_allowed': self.config['max_circuit_depth'],
                'description': f"Circuit depth ({circuit_depth}) exceeds maximum allowed ({self.config['max_circuit_depth']})",
                'timestamp': datetime.utcnow().isoformat()
            })
        
        # Check for potential infinite loops
        self._check_for_loops(operations, result)
    
    def _check_for_loops(self, operations: List[Any], result: Dict[str, Any]) -> None:
        """Check for potential infinite loops in operations."""
        # Simple heuristic: look for patterns that might indicate loops
        op_patterns = {}
        
        for i, operation in enumerate(operations):
            op_str = str(operation)
            if op_str in op_patterns:
                op_patterns[op_str].append(i)
            else:
                op_patterns[op_str] = [i]
        
        # Check for repeated operations that might indicate loops
        for op_str, indices in op_patterns.items():
            if len(indices) > 10:  # Arbitrary threshold
                result['warnings'].append({
                    'type': 'potential_loop',
                    'severity': 'low',
                    'operation': op_str,
                    'occurrences': len(indices),
                    'description': f"Operation '{op_str}' appears {len(indices)} times, possible loop",
                    'timestamp': datetime.utcnow().isoformat()
                })
    
    def _calculate_security_score(self, result: Dict[str, Any]) -> int:
        """Calculate a security score based on violations and warnings."""
        score = 100
        
        # Deduct points for violations
        for violation in result['violations']:
            severity = violation.get('severity', 'low')
            if severity == 'critical':
                score -= 30
            elif severity == 'high':
                score -= 20
            elif severity == 'medium':
                score -= 10
            elif severity == 'low':
                score -= 5
        
        # Deduct points for warnings
        for warning in result['warnings']:
            score -= 2
        
        return max(0, score)  # Ensure score doesn't go below 0
    
    def validate_state_management(self, state_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate quantum state management operations."""
        validation_result = {
            'state_id': state_data.get('id', 'unknown'),
            'validator_id': self.validator_id,
            'timestamp': datetime.utcnow().isoformat(),
            'is_valid': True,
            'violations': [],
            'security_score': 100
        }
        
        try:
            # Validate state structure
            required_fields = ['id', 'data']
            for field in required_fields:
                if field not in state_data:
                    validation_result['violations'].append({
                        'type': 'missing_state_field',
                        'severity': 'high',
                        'field': field,
                        'description': f"Required state field '{field}' is missing",
                        'timestamp': datetime.utcnow().isoformat()
                    })
                    validation_result['is_valid'] = False
            
            # Validate state data integrity
            if 'data' in state_data:
                self._validate_state_data(state_data['data'], validation_result)
            
            # Calculate security score
            validation_result['security_score'] = self._calculate_security_score(validation_result)
            
        except Exception as e:
            self.logger.error(f"State validation failed: {e}")
            validation_result['is_valid'] = False
            validation_result['violations'].append({
                'type': 'state_validation_error',
                'severity': 'critical',
                'description': f"State validation failed: {e}",
                'timestamp': datetime.utcnow().isoformat()
            })
        
        return validation_result
    
    def _validate_state_data(self, data: Any, result: Dict[str, Any]) -> None:
        """Validate quantum state data."""
        # Check data size (prevent memory exhaustion)
        data_str = json.dumps(data) if not isinstance(data, str) else data
        data_size = len(data_str.encode('utf-8'))
        
        max_size = 1024 * 1024  # 1MB limit
        if data_size > max_size:
            result['violations'].append({
                'type': 'state_data_too_large',
                'severity': 'high',
                'size': data_size,
                'max_allowed': max_size,
                'description': f"State data size ({data_size} bytes) exceeds maximum ({max_size} bytes)",
                'timestamp': datetime.utcnow().isoformat()
            })
        
        # Check for dangerous data patterns
        if isinstance(data, str) and self._is_dangerous_argument(data):
            result['violations'].append({
                'type': 'dangerous_state_data',
                'severity': 'high',
                'description': "State data contains potentially dangerous patterns",
                'timestamp': datetime.utcnow().isoformat()
            })
    
    def create_circuit_signature(self, circuit: Dict[str, Any]) -> str:
        """Create a cryptographic signature for a circuit."""
        # Create a deterministic representation of the circuit
        circuit_copy = circuit.copy()
        
        # Remove volatile fields
        circuit_copy.pop('timestamp', None)
        circuit_copy.pop('signature', None)
        
        # Create hash
        circuit_json = json.dumps(circuit_copy, sort_keys=True)
        signature = hashlib.sha256(circuit_json.encode('utf-8')).hexdigest()
        
        return signature
    
    def verify_circuit_signature(self, circuit: Dict[str, Any], expected_signature: str) -> bool:
        """Verify a circuit's cryptographic signature."""
        actual_signature = self.create_circuit_signature(circuit)
        return actual_signature == expected_signature