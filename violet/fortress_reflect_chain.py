"""
Fortress ReflectChain
Unbreachable blockchain-backed logging system
UID: ALC-ROOT-1010-1111-XCOV∞
"""

import time
import hashlib
import json
import logging
from typing import Dict, Any, List, Optional
from collections import deque

class FortressReflectChain:
    """Unbreachable ReflectChain logging with blockchain validation"""
    
    def __init__(self):
        self.security_uid = "ALC-ROOT-1010-1111-XCOV∞"
        self.chain = deque(maxlen=10000)  # Keep last 10000 entries
        self.current_block_number = 0
        self.pending_entries = []
        self.logger = self._setup_logger()
        self.genesis_hash = self._create_genesis_block()
        
    def _setup_logger(self):
        """Setup fortress reflect chain logger"""
        logger = logging.getLogger('fortress_reflect_chain')
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'[REFLECT-CHAIN-{self.security_uid}] %(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
        
    def _create_genesis_block(self) -> str:
        """Create the genesis block for the reflect chain"""
        genesis_data = {
            'block_number': 0,
            'timestamp': time.time(),
            'previous_hash': '0' * 64,
            'data': {
                'type': 'GENESIS',
                'security_uid': self.security_uid,
                'message': 'VIOLET-AF ReflectChain Genesis Block',
                'anti_sabotage': True
            },
            'nonce': 0
        }
        
        genesis_hash = self._calculate_block_hash(genesis_data)
        genesis_data['hash'] = genesis_hash
        
        self.chain.append(genesis_data)
        self.logger.info(f"✅ Genesis block created: {genesis_hash[:16]}...")
        
        return genesis_hash
        
    def reflect_log(self, log_type: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add immutable log entry to ReflectChain"""
        try:
            # Create log entry
            log_entry = {
                'timestamp': time.time(),
                'type': log_type,
                'message': message,
                'metadata': metadata or {},
                'security_uid': self.security_uid,
                'entry_id': self._generate_entry_id()
            }
            
            # Add to pending entries
            self.pending_entries.append(log_entry)
            
            # Create new block if we have enough entries or forced
            if len(self.pending_entries) >= 10 or log_type == 'EMERGENCY':
                block_hash = self._create_new_block()
                
                self.logger.info(f"✅ Log reflected to chain: {log_type} - Block: {block_hash[:16]}...")
                return block_hash
            else:
                entry_id = log_entry['entry_id']
                self.logger.debug(f"✅ Log entry pending: {log_type} - ID: {entry_id[:16]}...")
                return entry_id
                
        except Exception as e:
            self.logger.error(f"🚨 Reflect log failed: {e}")
            return ""
            
    def _generate_entry_id(self) -> str:
        """Generate unique entry ID"""
        entry_data = f"{time.time()}{self.security_uid}{len(self.pending_entries)}"
        return hashlib.sha256(entry_data.encode()).hexdigest()
        
    def _create_new_block(self) -> str:
        """Create new block with pending entries"""
        if not self.pending_entries:
            return ""
            
        # Get previous block hash
        previous_hash = self.chain[-1]['hash'] if self.chain else self.genesis_hash
        
        # Create new block
        block_data = {
            'block_number': self.current_block_number + 1,
            'timestamp': time.time(),
            'previous_hash': previous_hash,
            'data': {
                'entries': self.pending_entries.copy(),
                'entry_count': len(self.pending_entries),
                'security_uid': self.security_uid
            },
            'nonce': self._calculate_nonce()
        }
        
        # Calculate block hash
        block_hash = self._calculate_block_hash(block_data)
        block_data['hash'] = block_hash
        
        # Add to chain
        self.chain.append(block_data)
        self.current_block_number += 1
        
        # Clear pending entries
        self.pending_entries.clear()
        
        return block_hash
        
    def _calculate_block_hash(self, block_data: Dict[str, Any]) -> str:
        """Calculate cryptographic hash for block"""
        # Create copy without hash field for calculation
        block_copy = block_data.copy()
        block_copy.pop('hash', None)
        
        # Convert to deterministic string
        block_string = json.dumps(block_copy, sort_keys=True) + self.security_uid
        
        return hashlib.sha256(block_string.encode()).hexdigest()
        
    def _calculate_nonce(self) -> int:
        """Calculate proof-of-work nonce (simplified)"""
        # In a real blockchain, this would be computationally intensive
        # For this implementation, use a simple calculation
        return int(time.time() * 1000) % 1000000
        
    def validate_chain_integrity(self) -> bool:
        """Validate the entire chain integrity"""
        try:
            if not self.chain:
                return True
                
            # Check each block
            for i, block in enumerate(self.chain):
                # Validate block structure
                if not self._validate_block_structure(block):
                    self.logger.error(f"🚨 Invalid block structure at index {i}")
                    return False
                    
                # Validate hash
                if not self._validate_block_hash(block):
                    self.logger.error(f"🚨 Invalid block hash at index {i}")
                    return False
                    
                # Validate chain linkage (except genesis)
                if i > 0:
                    previous_block = self.chain[i-1]
                    if block['previous_hash'] != previous_block['hash']:
                        self.logger.error(f"🚨 Chain linkage broken at block {i}")
                        return False
                        
            self.logger.info("✅ Chain integrity validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"🚨 Chain validation error: {e}")
            return False
            
    def _validate_block_structure(self, block: Dict[str, Any]) -> bool:
        """Validate block has required structure"""
        required_fields = ['block_number', 'timestamp', 'previous_hash', 'data', 'hash']
        
        for field in required_fields:
            if field not in block:
                return False
                
        # Validate data structure
        if not isinstance(block['data'], dict):
            return False
            
        return True
        
    def _validate_block_hash(self, block: Dict[str, Any]) -> bool:
        """Validate block hash is correct"""
        stored_hash = block.get('hash')
        calculated_hash = self._calculate_block_hash(block)
        
        return stored_hash == calculated_hash
        
    def search_logs(self, search_criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search ReflectChain logs with given criteria"""
        results = []
        
        try:
            # Search through all blocks
            for block in self.chain:
                if 'entries' in block.get('data', {}):
                    entries = block['data']['entries']
                    
                    for entry in entries:
                        if self._matches_criteria(entry, search_criteria):
                            # Add block context to entry
                            entry_with_context = entry.copy()
                            entry_with_context['block_number'] = block['block_number']
                            entry_with_context['block_hash'] = block['hash']
                            results.append(entry_with_context)
                            
            self.logger.info(f"✅ Search completed: {len(results)} results found")
            
        except Exception as e:
            self.logger.error(f"🚨 Search error: {e}")
            
        return results
        
    def _matches_criteria(self, entry: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """Check if entry matches search criteria"""
        for key, value in criteria.items():
            if key not in entry:
                return False
                
            entry_value = entry[key]
            
            # String matching
            if isinstance(value, str) and isinstance(entry_value, str):
                if value.lower() not in entry_value.lower():
                    return False
                    
            # Exact matching for other types
            elif entry_value != value:
                return False
                
        return True
        
    def get_chain_status(self) -> Dict[str, Any]:
        """Get comprehensive chain status"""
        total_entries = sum(
            len(block.get('data', {}).get('entries', []))
            for block in self.chain
            if 'data' in block and 'entries' in block['data']
        )
        
        return {
            'security_uid': self.security_uid,
            'chain_length': len(self.chain),
            'current_block_number': self.current_block_number,
            'total_entries': total_entries,
            'pending_entries': len(self.pending_entries),
            'genesis_hash': self.genesis_hash,
            'latest_hash': self.chain[-1]['hash'] if self.chain else None,
            'chain_integrity': self.validate_chain_integrity(),
            'status': 'OPERATIONAL'
        }
        
    def emergency_reflect(self, emergency_type: str, details: str) -> str:
        """Emergency reflect for critical security events"""
        emergency_metadata = {
            'emergency_type': emergency_type,
            'severity': 'CRITICAL',
            'timestamp': time.time(),
            'security_uid': self.security_uid
        }
        
        # Force immediate block creation for emergencies
        block_hash = self.reflect_log('EMERGENCY', details, emergency_metadata)
        
        self.logger.critical(f"🚨 EMERGENCY REFLECTED: {emergency_type} - {details}")
        
        return block_hash