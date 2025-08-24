"""
ReflectLogger - UID-stamped logging system for VIOLET-AF
UID: ALC-ROOT-1010-1111-XCOV∞
Domain: Kidhum
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any


class ReflectLogger:
    def __init__(self, uid="ALC-ROOT-1010-1111-XCOV∞", state_file_path=None):
        self.uid = uid
        self.state_file_path = state_file_path or "/home/runner/work/Satan/Satan/config/VioletState.json"
        self.log_blocks = []
        self.memory_state = {}
        
    def create_log_block(self, event_type: str, data: Dict[str, Any], quantum_stamps: List[Dict] = None) -> Dict[str, Any]:
        """Create a UID-stamped log block for ReflectChain"""
        timestamp = datetime.now().isoformat()
        log_block = {
            'uid': self.uid,
            'block_id': f'REFL-{self.uid}-{len(self.log_blocks)}-{timestamp}',
            'timestamp': timestamp,
            'event_type': event_type,
            'data': data,
            'quantum_stamps': quantum_stamps or [],
            'sequence_number': len(self.log_blocks)
        }
        
        self.log_blocks.append(log_block)
        self._update_memory_state(log_block)
        return log_block
    
    def log_quantum_execution(self, quantum_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Log quantum circuit execution with reflect stamps"""
        return self.create_log_block(
            event_type='quantum_execution',
            data=quantum_summary,
            quantum_stamps=quantum_summary.get('reflect_stamps', [])
        )
    
    def log_task_execution(self, task_type: str, task_data: Dict[str, Any], success: bool = True) -> Dict[str, Any]:
        """Log automation task execution"""
        return self.create_log_block(
            event_type='task_execution',
            data={
                'task_type': task_type,
                'task_data': task_data,
                'success': success,
                'execution_context': 'violet_automation'
            }
        )
    
    def log_system_event(self, event_name: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Log general system events"""
        return self.create_log_block(
            event_type='system_event',
            data={
                'event_name': event_name,
                'details': details
            }
        )
    
    def _update_memory_state(self, log_block: Dict[str, Any]):
        """Update ReflectChain memory state with new log block"""
        # Update memory state based on log block type
        event_type = log_block['event_type']
        
        if event_type == 'quantum_execution':
            self.memory_state['last_quantum_execution'] = log_block['timestamp']
            self.memory_state['quantum_executions_count'] = self.memory_state.get('quantum_executions_count', 0) + 1
            
        elif event_type == 'task_execution':
            task_type = log_block['data']['task_type']
            self.memory_state[f'last_{task_type}'] = log_block['timestamp']
            self.memory_state['total_tasks'] = self.memory_state.get('total_tasks', 0) + 1
            
        # Store recent blocks for quick access
        if 'recent_blocks' not in self.memory_state:
            self.memory_state['recent_blocks'] = []
        
        self.memory_state['recent_blocks'].append(log_block['block_id'])
        # Keep only last 10 block IDs
        self.memory_state['recent_blocks'] = self.memory_state['recent_blocks'][-10:]
    
    def save_to_violet_state(self):
        """Save log blocks to VioletState.json"""
        try:
            # Load current state
            with open(self.state_file_path, 'r') as f:
                state = json.load(f)
            
            # Update reflect_chain section
            state['reflect_chain']['log_blocks'] = self.log_blocks
            state['reflect_chain']['memory_state'] = self.memory_state
            state['reflect_chain']['last_update'] = datetime.now().isoformat()
            
            # Save updated state
            with open(self.state_file_path, 'w') as f:
                json.dump(state, f, indent=2)
                
        except Exception as e:
            # If state file doesn't exist, create basic structure
            os.makedirs(os.path.dirname(self.state_file_path), exist_ok=True)
            state = {
                'uid': self.uid,
                'reflect_chain': {
                    'enabled': True,
                    'log_blocks': self.log_blocks,
                    'memory_state': self.memory_state,
                    'last_update': datetime.now().isoformat()
                }
            }
            with open(self.state_file_path, 'w') as f:
                json.dump(state, f, indent=2)
    
    def get_memory_state(self) -> Dict[str, Any]:
        """Get current ReflectChain memory state"""
        return self.memory_state.copy()
    
    def get_log_blocks(self, event_type: str = None, limit: int = None) -> List[Dict[str, Any]]:
        """Get log blocks, optionally filtered by event type"""
        blocks = self.log_blocks
        
        if event_type:
            blocks = [block for block in blocks if block['event_type'] == event_type]
            
        if limit:
            blocks = blocks[-limit:]
            
        return blocks
    
    def get_recent_quantum_stamps(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent quantum stamps from log blocks"""
        stamps = []
        for block in reversed(self.log_blocks):
            if block.get('quantum_stamps'):
                stamps.extend(block['quantum_stamps'])
                if len(stamps) >= limit:
                    break
        return stamps[:limit]
    
    def clear_logs(self):
        """Clear all log blocks (use with caution)"""
        self.log_blocks = []
        self.memory_state = {}
    
    def export_logs(self, filepath: str = None) -> str:
        """Export all logs to a JSON file"""
        if filepath is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f"/home/runner/work/Satan/Satan/quantum/reflect_logs_{timestamp}.json"
            
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        export_data = {
            'uid': self.uid,
            'export_timestamp': datetime.now().isoformat(),
            'log_blocks': self.log_blocks,
            'memory_state': self.memory_state,
            'total_blocks': len(self.log_blocks)
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
            
        return filepath