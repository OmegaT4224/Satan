"""
VIOLET-AF Quantum Logic System
Main package for quantum automation and security integration
"""

from .quantum_engine import VioletQuantumEngine
from .circuit_builder import CircuitBuilder
from .state_interpreter import StateInterpreter
from .reflect_chain_binder import ReflectChainBinder
from .violet_launcher import VioletLauncher, launch

__version__ = "1.0.0"
__uid__ = "ALC-ROOT-1010-1111-XCOV∞"

__all__ = [
    "VioletQuantumEngine",
    "CircuitBuilder", 
    "StateInterpreter",
    "ReflectChainBinder",
    "VioletLauncher",
    "launch"
]