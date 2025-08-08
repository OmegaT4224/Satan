"""
VIOLET Launcher - Main execution trigger for VIOLET-AF
UID: ALC-ROOT-1010-1111-XCOV∞
Domain: Kidhum
"""

from datetime import datetime
from typing import Dict, Any, Optional
from .axiom_dev_core import AxiomDevCore


def violet_launch(uid: str = "ALC-ROOT-1010-1111-XCOV∞", 
                 parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Main execution trigger for VIOLET-AF quantum automation system
    
    Args:
        uid: Unique identifier for the execution (must match ALC-ROOT-1010-1111-XCOV∞)
        parameters: Optional parameters for customization
    
    Returns:
        Dict containing execution results and system status
    """
    expected_uid = "ALC-ROOT-1010-1111-XCOV∞"
    
    # Validate UID
    if uid != expected_uid:
        return {
            'success': False,
            'error': f'Invalid UID. Expected: {expected_uid}, Received: {uid}',
            'timestamp': datetime.now().isoformat(),
            'operation': 'violet_launch'
        }
    
    # Initialize parameters if not provided
    if parameters is None:
        parameters = {}
    
    try:
        # Create AxiomDevCore instance
        axiom_core = AxiomDevCore(uid=uid)
        
        # Initialize system
        init_result = axiom_core.initialize_system()
        
        if not init_result['success']:
            return {
                'success': False,
                'error': 'System initialization failed',
                'init_result': init_result,
                'timestamp': datetime.now().isoformat(),
                'operation': 'violet_launch'
            }
        
        # Execute quantum automation
        automation_result = axiom_core.execute_quantum_automation()
        
        # Get final system status
        system_status = axiom_core.get_system_status()
        
        # Prepare success response
        launch_result = {
            'success': True,
            'uid': uid,
            'domain': 'Kidhum',
            'timestamp': datetime.now().isoformat(),
            'operation': 'violet_launch',
            'initialization': init_result,
            'quantum_automation': automation_result,
            'system_status': system_status,
            'parameters': parameters,
            'violet_state_binding': {
                'final_quantum_state': automation_result.get('quantum_measurement'),
                'reflect_log_blocks': system_status['reflect_logs_count'],
                'kidhum_deploy_command': f"kidhum deploy --uid={uid}",
                'successful_execution': True
            }
        }
        
        # Log the launch
        axiom_core.reflect_logger.log_system_event('violet_launch_completed', {
            'uid': uid,
            'parameters': parameters,
            'success': True,
            'results': launch_result
        })
        
        # Save final state
        axiom_core.reflect_logger.save_to_violet_state()
        
        return launch_result
        
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'uid': uid,
            'timestamp': datetime.now().isoformat(),
            'operation': 'violet_launch',
            'parameters': parameters
        }
        
        return error_result


def violet_status(uid: str = "ALC-ROOT-1010-1111-XCOV∞") -> Dict[str, Any]:
    """
    Get current status of VIOLET-AF system
    
    Args:
        uid: System UID
        
    Returns:
        Dict containing current system status
    """
    expected_uid = "ALC-ROOT-1010-1111-XCOV∞"
    
    if uid != expected_uid:
        return {
            'success': False,
            'error': f'Invalid UID. Expected: {expected_uid}, Received: {uid}',
            'timestamp': datetime.now().isoformat(),
            'operation': 'violet_status'
        }
    
    try:
        # Create temporary AxiomDevCore instance for status check
        axiom_core = AxiomDevCore(uid=uid)
        status = axiom_core.get_system_status()
        
        return {
            'success': True,
            'uid': uid,
            'operation': 'violet_status',
            'timestamp': datetime.now().isoformat(),
            'status': status
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'uid': uid,
            'timestamp': datetime.now().isoformat(),
            'operation': 'violet_status'
        }


def violet_reset(uid: str = "ALC-ROOT-1010-1111-XCOV∞", 
                confirm: bool = False) -> Dict[str, Any]:
    """
    Reset VIOLET-AF system (use with caution)
    
    Args:
        uid: System UID
        confirm: Must be True to actually perform reset
        
    Returns:
        Dict containing reset results
    """
    expected_uid = "ALC-ROOT-1010-1111-XCOV∞"
    
    if uid != expected_uid:
        return {
            'success': False,
            'error': f'Invalid UID. Expected: {expected_uid}, Received: {uid}',
            'timestamp': datetime.now().isoformat(),
            'operation': 'violet_reset'
        }
    
    if not confirm:
        return {
            'success': False,
            'error': 'Reset requires explicit confirmation (confirm=True)',
            'timestamp': datetime.now().isoformat(),
            'operation': 'violet_reset'
        }
    
    try:
        # Create AxiomDevCore instance
        axiom_core = AxiomDevCore(uid=uid)
        
        # Clear logs and reset state
        axiom_core.reflect_logger.clear_logs()
        axiom_core.content_writer.clear_generated_files()
        
        # Log the reset
        axiom_core.reflect_logger.log_system_event('system_reset', {
            'uid': uid,
            'reset_timestamp': datetime.now().isoformat(),
            'performed_by': 'violet_reset_function'
        })
        
        # Save state
        axiom_core.reflect_logger.save_to_violet_state()
        
        return {
            'success': True,
            'uid': uid,
            'operation': 'violet_reset',
            'timestamp': datetime.now().isoformat(),
            'message': 'System reset completed successfully'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'uid': uid,
            'timestamp': datetime.now().isoformat(),
            'operation': 'violet_reset'
        }


# Main interface functions for external use
__all__ = ['violet_launch', 'violet_status', 'violet_reset']