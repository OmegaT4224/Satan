"""
VIOLET-AF: Autonomous Quantum Logic Implementation
UID: ALC-ROOT-1010-1111-XCOV∞
Domain: Kidhum

Core quantum automation system package.
"""

from .quantum_engine import QuantumEngine
from .axiom_dev_core import AxiomDevCore
from .gh_agent import GitHubAgent
from .reflect_logger import ReflectLogger
from .content_writer import ContentWriter
from .violet_launcher import violet_launch, violet_status, violet_reset

__version__ = "1.0.0"
__uid__ = "ALC-ROOT-1010-1111-XCOV∞"
__domain__ = "Kidhum"

__all__ = [
    'QuantumEngine',
    'AxiomDevCore', 
    'GitHubAgent',
    'ReflectLogger',
    'ContentWriter',
    'violet_launch',
    'violet_status',
    'violet_reset'
]