"""
VIOLET-AF Circuit Builder
Builds the specific H/CNOT/Z quantum sequence
"""
from typing import List, Tuple


class CircuitBuilder:
    """Build quantum circuits for VIOLET-AF sequence"""
    
    def __init__(self):
        self.circuit_instructions = []
        
    def build_violet_sequence(self) -> List[Tuple[str, int, int]]:
        """Build the complete VIOLET-AF quantum circuit sequence"""
        sequence = [
            ("H", 0, None),      # Hadamard superposition
            ("CNOT", 0, 1),      # Entanglement link
            ("H", 0, None),      # Recursive superposition
            ("CNOT", 0, 1),      # Task tree expansion
            ("H", 0, None),      # Symbolic recursion
            ("CNOT", 0, 1),      # Memory binding
            ("H", 0, None),      # ReflectChain trigger
            ("CNOT", 0, 1),      # UID stamp preparation
            ("H", 0, None),      # Final superposition
            ("Z", 0, None),      # Log stamp q_0
            ("Z", 1, None),      # Log stamp q_1
            ("Z", 2, None),      # Log stamp q_2 (FINAL SEAL)
        ]
        
        self.circuit_instructions = sequence
        return sequence
        
    def get_circuit_depth(self) -> int:
        """Get the depth of the quantum circuit"""
        return len(self.circuit_instructions)
        
    def get_gate_counts(self) -> dict:
        """Get count of each gate type in the circuit"""
        counts = {"H": 0, "CNOT": 0, "Z": 0}
        for gate, _, _ in self.circuit_instructions:
            if gate in counts:
                counts[gate] += 1
        return counts
        
    def validate_circuit(self) -> bool:
        """Validate the VIOLET-AF circuit meets specifications"""
        expected_gates = {"H": 5, "CNOT": 4, "Z": 3}
        actual_gates = self.get_gate_counts()
        return expected_gates == actual_gates