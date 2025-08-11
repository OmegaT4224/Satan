"""
VIOLET-AF Security System
Anti-sabotage protection and quantum security validation
"""

from .quantum_security import QuantumSecurity
from .anti_sabotage_monitor import ThreatDetectionEngine
from .encrypted_state_manager import EncryptedStateManager
from .uid_validator import UIDValidator

__version__ = "1.0.0"
__uid__ = "ALC-ROOT-1010-1111-XCOV∞"

__all__ = [
    "QuantumSecurity",
    "ThreatDetectionEngine",
    "EncryptedStateManager", 
    "UIDValidator"
]